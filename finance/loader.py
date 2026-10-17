"""Lê snapshots normalizados, conserva a origem e valida antes de calcular."""
import calendar
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
from pathlib import Path
import re


class ValidationError(ValueError):
    pass


FIELDS = {
    'peps': 'pep pai projeto descricao responsavel',
    'baseline': 'id versao pep periodo classe_custo valor_brl',
    'cji3': 'id pep data empresa exercicio documento item classe_custo descricao valor_brl natureza pedido item_pedido',
    'cji5': 'id pep data_snapshot tipo documento item alocacao classe_custo descricao data_prevista valor_brl',
    'cjia': 'id pep data tipo empresa exercicio documento item classe_custo descricao valor_brl pedido item_pedido',
    'etc': 'id versao pep periodo classe_custo valor_brl premissa responsavel',
    'conciliacoes': 'id custo_id pagamento_id valor_brl',
    'conferencia': 'id fonte pep classe_custo data_snapshot realizado_brl compromisso_brl orcamento_brl plan_re_brl disposto_brl comparavel escopo',
}
SAFE_LIMIT = 9_007_199_254_740_991


def require(ok, message):
    if not ok:
        raise ValidationError(message)


def iso_date(value):
    try:
        parsed = date.fromisoformat(value)
        require(parsed.isoformat() == value, 'Data deve estar em AAAA-MM-DD.')
        return value
    except (ValueError, TypeError) as exc:
        raise ValidationError(f'Data inválida: {value!r}.') from exc


def period(value):
    require(bool(re.fullmatch(r'[0-9]{4}-(0[1-9]|1[0-2])', value)), f'Período inválido: {value!r}.')
    iso_date(value+'-01')
    return value


def cents(value):
    require(bool(re.fullmatch(r'-?[0-9]+(?:\.[0-9]{1,2})?', value)), f'Valor inválido: {value!r}; use ponto e até duas casas decimais.')
    try:
        result = int(Decimal(value)*100)
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError('Valor monetário inválido.') from exc
    require(abs(result) <= SAFE_LIMIT, 'Valor ultrapassa limite de inteiro seguro.')
    return result


def load_bundle(input_dir, manifest_path):
    root = Path(input_dir).resolve()
    try:
        raw_manifest = Path(manifest_path).read_bytes()
        manifest = json.loads(raw_manifest.decode('utf-8-sig'))
    except (OSError, ValueError, UnicodeError) as exc:
        raise ValidationError(f'Manifesto indisponível ou inválido: {exc}') from exc
    require(isinstance(manifest, dict), 'Manifesto deve ser um objeto JSON.')
    cut = iso_date(manifest.get('data_corte'))
    parsed = date.fromisoformat(cut)
    require(parsed.day == calendar.monthrange(parsed.year, parsed.month)[1], 'Corte deve ser o último dia do mês.')
    require(manifest.get('moeda') == 'BRL', 'Esta versão aceita apenas BRL.')
    approval = iso_date(manifest.get('data_aprovacao_baseline'))
    require(approval <= cut, 'Aprovação da baseline posterior ao corte.')
    for field in ('versao_baseline', 'versao_forecast', 'escopo'):
        require(isinstance(manifest.get(field), str) and manifest[field].strip(), f'Manifesto: {field} obrigatório.')
    require(isinstance(manifest.get('dados_ficticios'), bool), 'Declare dados_ficticios como true ou false.')
    files = manifest.get('arquivos', {})
    require(isinstance(files, dict) and set(files) == set(FIELDS), 'Manifesto deve declarar os oito arquivos de entrada.')
    require(all(isinstance(v, str) for v in files.values()), 'Nomes dos arquivos devem ser texto.')
    require(len(set(files.values())) == len(files), 'Arquivos de entrada duplicados no manifesto.')
    tables, sources = {}, {}
    for kind, fields in FIELDS.items():
        filename = files[kind]
        require(isinstance(filename, str) and filename and not any(c in filename for c in '/\\:') and filename not in ('.','..'), 'Use nomes de arquivo locais, sem caminho.')
        path = (root/filename).resolve()
        require(path.parent == root and not (root/filename).is_symlink(), 'Arquivo fora da pasta de entrada.')
        try:
            raw = path.read_bytes()
            require(len(raw) <= 25*1024*1024, f'{filename}: limite de 25 MiB.')
            reader = csv.DictReader(io.StringIO(raw.decode('utf-8-sig'), newline=''), delimiter=';')
            require(reader.fieldnames is not None and len(reader.fieldnames) == len(set(reader.fieldnames)), f'{filename}: cabeçalhos ausentes/duplicados.')
            require(set(fields.split()) <= set(reader.fieldnames), f'{filename}: colunas esperadas: {fields}.')
            rows = []
            line = 2
            for row in reader:
                require(None not in row and all(row.get(k) is not None for k in fields.split()), f'{filename}:{line}: número de campos inconsistente.')
                cleaned = {k: row[k].strip() for k in fields.split()}
                require(all(len(v) <= 2000 for v in cleaned.values()), f'{filename}:{line}: campo muito longo.')
                cleaned.update(source_file=filename, source_line=line)
                rows.append(cleaned)
                line = reader.line_num+1
                require(len(rows) <= 50_000, f'{filename}: limite de 50.000 linhas.')
        except (OSError, UnicodeError, csv.Error) as exc:
            raise ValidationError(f'{filename}: não foi possível ler o CSV: {exc}') from exc
        tables[kind] = rows
        sources[filename] = {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw), 'rows': len(rows), 'role': kind}
    peps = tables['peps']
    require(bool(peps), 'Cadastre pelo menos um PEP.')
    by_pep = {}
    for p in peps:
        require(p['pep'] and p['projeto'] and p['descricao'] and p['responsavel'], 'Cadastro PEP incompleto.')
        require(p['pep'] not in by_pep, 'PEP duplicado.')
        by_pep[p['pep']] = p
    parents = {p['pai'] for p in peps if p['pai']}
    for p in peps:
        seen = {p['pep']}
        current = p
        while current['pai']:
            require(current['pai'] in by_pep, 'Pai PEP inexistente.')
            require(current['pai'] not in seen, 'Hierarquia PEP contém ciclo.')
            current = by_pep[current['pai']]
            require(current['projeto'] == p['projeto'], 'Pai e filho devem pertencer ao mesmo projeto.')
            seen.add(current['pep'])
        p['leaf'] = p['pep'] not in parents
    facts, ids, natural = [], set(), set()
    for table in ('baseline', 'cji3', 'cji5', 'cjia', 'etc'):
        for row in tables[table]:
            where = f"{row['source_file']}:{row['source_line']}"
            require(row['id'] and row['id'] not in ids, f'{where}: ID duplicado ou vazio; IDs financeiros são globais.')
            ids.add(row['id'])
            require(row['pep'] in by_pep, f'{where}: PEP desconhecido.')
            require(by_pep[row['pep']]['leaf'], f'{where}: valores somente em PEP folha.')
            require(bool(row['classe_custo']), f'{where}: classe de custo obrigatória.')
            value = cents(row['valor_brl'])
            fact = dict(row, value=value, table=table, project=by_pep[row['pep']]['projeto'])
            if table in ('baseline', 'etc'):
                key = 'versao_baseline' if table == 'baseline' else 'versao_forecast'
                require(row['versao'] == manifest[key], f'{where}: versão diferente do manifesto.')
                fact.update(kind='BASELINE' if table == 'baseline' else 'ETC', date=period(row['periodo'])+'-01')
                require(value >= 0, f'{where}: baseline/ETC deve ser não negativo.')
                if table == 'etc':
                    require(row['periodo'] > cut[:7], f'{where}: ETC precisa estar após o mês de corte.')
                    require(row['premissa'] and row['responsavel'], f'{where}: ETC exige premissa e responsável.')
                nk = (table, row['versao'], row['pep'], row['periodo'], row['classe_custo'])
            elif table == 'cji5':
                require(iso_date(row['data_snapshot']) == cut, f'{where}: snapshot CJI5 diferente do corte.')
                require(row['tipo'] in ('RC','PC'), f'{where}: tipo CJI5 deve ser RC ou PC.')
                require(value >= 0, f'{where}: compromisso residual negativo exige revisão do extrato.')
                require(row['documento'] and row['item'] and row['alocacao'], f'{where}: documento, item e alocação obrigatórios.')
                fact.update(kind='COMPROMISSO', date=iso_date(row['data_prevista']))
                nk = (table, row['tipo'], row['documento'], row['item'], row['alocacao'])
            else:
                iso_date(row['data'])
                require(row['empresa'] and row['documento'] and row['item'], f'{where}: chave de documento incompleta.')
                require(bool(re.fullmatch(r'[0-9]{4}', row['exercicio'])), f'{where}: exercício inválido.')
                require(bool(row['pedido']) == bool(row['item_pedido']), f'{where}: informe pedido e item juntos.')
                if table == 'cji3':
                    require(row['natureza'] in ('CUSTO','LIQUIDACAO'), f'{where}: natureza CJI3 não reconhecida.')
                    fact['kind'] = 'REALIZADO' if row['natureza'] == 'CUSTO' else 'LIQUIDACAO'
                else:
                    require(row['tipo'] in ('PAGAMENTO','COMPROMISSO_PAGAMENTO'), f'{where}: natureza CJIA não reconhecida.')
                    fact['kind'] = row['tipo']
                    require(fact['kind'] != 'COMPROMISSO_PAGAMENTO' or value >= 0, f'{where}: compromisso de caixa negativo não suportado.')
                require(fact['kind'] == 'COMPROMISSO_PAGAMENTO' or row['data'] <= cut, f'{where}: realizado/pagamento posterior ao corte.')
                fact['date'] = row['data']
                nk = (table, row['empresa'], row['exercicio'], row['documento'], row['item'], row['pep'])
            require(nk not in natural, f'{where}: chave natural duplicada.')
            natural.add(nk)
            facts.append(fact)
    require(sum(abs(f['value']) for f in facts) <= SAFE_LIMIT, 'Soma ultrapassa limite de inteiro seguro.')
    by_id = {f['id']: f for f in facts}
    allocations, pairs, link_ids, allocated = [], set(), set(), {}
    for row in tables['conciliacoes']:
        require(row['id'] and row['id'] not in link_ids, 'Conciliação com ID duplicado/vazio.')
        link_ids.add(row['id'])
        a, p = by_id.get(row['custo_id']), by_id.get(row['pagamento_id'])
        require(a and p and a['kind'] == 'REALIZADO' and p['kind'] == 'PAGAMENTO', 'Conciliação exige custo CJI3 e pagamento realizado CJIA existentes.')
        require((a['pep'],a['classe_custo']) == (p['pep'],p['classe_custo']), 'Conciliação exige mesmo PEP e classe de custo.')
        require(a['empresa'] == p['empresa'], 'Conciliação entre empresas não é suportada; confira a empresa dos documentos.')
        value = cents(row['valor_brl'])
        require(value != 0 and a['value']*value > 0 and p['value']*value > 0, 'Sinal da alocação incompatível com custo/pagamento.')
        pair = (a['id'],p['id'])
        require(pair not in pairs, 'Par de conciliação duplicado.')
        pairs.add(pair)
        for f in (a,p):
            allocated[f['id']] = allocated.get(f['id'],0)+value
            require(abs(allocated[f['id']]) <= abs(f['value']), 'Sobre-alocação: conciliação excede o documento.')
        allocations.append(dict(row, value=value, pep=a['pep'], classe_custo=a['classe_custo']))
    controls, control_ids, control_keys = [], set(), set()
    for row in tables['conferencia']:
        require(row['id'] and row['id'] not in control_ids, 'Conferência com ID duplicado/vazio.')
        control_ids.add(row['id'])
        require(row['pep'] in by_pep and by_pep[row['pep']]['leaf'], 'Conferência exige PEP folha cadastrado.')
        require(row['fonte'] and row['classe_custo'] and row['escopo'], 'Conferência exige fonte, classe e escopo.')
        require(iso_date(row['data_snapshot']) == cut, 'Snapshot de conferência diferente do corte.')
        require(row['comparavel'] in ('SIM','NAO'), 'Conferência: comparavel deve ser SIM ou NAO.')
        key=(row['fonte'],row['pep'],row['classe_custo'])
        require(key not in control_keys, 'Chave de conferência duplicada.')
        control_keys.add(key)
        actual_ref, commitment_ref = cents(row['realizado_brl']), cents(row['compromisso_brl'])
        require(commitment_ref >= 0, 'Compromisso de referência deve ser não negativo.')
        extra={key:cents(row[col]) if row[col] else None for key,col in [('budget_ref','orcamento_brl'),('remaining_plan_ref','plan_re_brl'),('assigned_ref','disposto_brl')]}
        require(extra['budget_ref'] is None or extra['budget_ref'] >= 0, 'Orçamento de referência não pode ser negativo.')
        controls.append(dict(row, actual_ref=actual_ref, commitment_ref=commitment_ref, **extra))
    require(sum(abs(f['value']) for f in facts)+sum(abs(c['actual_ref'])+c['commitment_ref']+sum(abs(c[k] or 0) for k in ('budget_ref','remaining_plan_ref','assigned_ref')) for c in controls) <= SAFE_LIMIT, 'Conjunto de fatos/referências ultrapassa limite de inteiro seguro.')
    return {'manifest': manifest, 'manifest_sha256': hashlib.sha256(raw_manifest).hexdigest(), 'peps': peps, 'facts': facts, 'matches': allocations, 'controls': controls, 'sources': sources}
