"""Gera arquivos locais; nenhuma chamada de rede ou conexão SAP."""
import csv
import json
from pathlib import Path
import sqlite3

from .engine import ROOT, calculate
from .loader import load_bundle, require


def safe_cell(value):
    if isinstance(value, str) and value.lstrip().startswith(('=','+','-','@')):
        return "'"+value
    return value


def render(report, prefix='./'):
    page = (ROOT/'web/template.html').read_text(encoding='utf-8')
    values = {
        '__CSS__': (ROOT/'web/style.css').read_text(encoding='utf-8'),
        '__METRICS__': (ROOT/'web/metrics.js').read_text(encoding='utf-8'),
        '__JS__': (ROOT/'web/app.js').read_text(encoding='utf-8'),
        '__DATA__': json.dumps(report, ensure_ascii=False, separators=(',',':')).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026'),
        '__CONTEXT__': json.dumps({'downloadPrefix':prefix}),
    }
    # Substituir marcadores em uma só passagem impede substituição dentro dos dados.
    import re
    return re.sub('|'.join(re.escape(k) for k in values), lambda m: values[m.group()], page)


def write_report(report, db, output):
    output.mkdir(parents=True, exist_ok=True)
    (output/'relatorio.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    (output/'index.html').write_text(render(report), encoding='utf-8')
    target = sqlite3.connect(output/'finance.sqlite')
    try:
        db.backup(target)
    finally:
        target.close()
    for filename, rows, fields in (
        ('fatos.csv', report['facts'], 'id kind pep date classe_custo value descricao documento item pedido item_pedido tipo versao premissa source_file source_line'),
        ('peps.csv', report['pep_metrics'], 'pep baseline baseline_cut actual commitment etc eac variance variance_cut paid cash_commitment matched actual_unmatched cash_unmatched'),
        ('conciliacoes.csv', report['matches'], 'id custo_id pagamento_id pep classe_custo value source_file source_line'),
        ('conferencia.csv', report['controls'], 'id fonte pep classe_custo budget_ref actual_ref actual_model delta_actual commitment_ref commitment_model delta_commitment remaining_plan_ref assigned_ref comparavel escopo source_file source_line'),
    ):
        with (output/filename).open('w',encoding='utf-8-sig',newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields.split(), delimiter=';', extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow({k:safe_cell(v) for k,v in row.items() if k in fields.split()})


def build(input_dir, manifest, output):
    source, target = Path(input_dir).resolve(), Path(output).resolve()
    require(not target.is_relative_to(source) and not source.is_relative_to(target), 'Saída não pode conter nem estar dentro da entrada.')
    require(not target.exists(), 'A saída já existe; escolha uma pasta nova.')
    report, db = calculate(load_bundle(source, manifest))
    try:
        write_report(report, db, target)
    finally:
        db.close()
    return report


def demo():
    bundle = load_bundle(ROOT/'sample-input', ROOT/'config/manifest.json')
    require(bundle['manifest']['dados_ficticios'], 'demo requer dados_ficticios=true; use build para dados locais.')
    report, db = calculate(bundle)
    try:
        write_report(report, db, ROOT/'reports/demo')
        (ROOT/'index.html').write_text(render(report,'./reports/demo/'), encoding='utf-8')
    finally:
        db.close()
    return report
