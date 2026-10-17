"""Views SQL efetivamente executadas e resultado auditável do snapshot."""
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from uuid import uuid4

from . import VERSION

ROOT = Path(__file__).resolve().parents[1]


def calculate(bundle):
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    db.executescript((ROOT/'sql/schema.sql').read_text(encoding='utf-8'))
    db.execute('INSERT INTO context VALUES (?)', (bundle['manifest']['data_corte'],))
    db.executemany('INSERT INTO peps VALUES (?,?,?,?,?,?)', [(p['pep'],p['pai'],p['projeto'],p['descricao'],p['responsavel'],p['leaf']) for p in bundle['peps']])
    db.executemany('INSERT INTO facts VALUES (?,?,?,?,?,?,?,?,?)', [(f['id'],f['pep'],f['kind'],f['date'],f['classe_custo'],f['value'],f['source_file'],f['source_line'],json.dumps(f,ensure_ascii=False)) for f in bundle['facts']])
    db.executemany('INSERT INTO matches VALUES (?,?,?,?,?,?)', [(m['id'],m['custo_id'],m['pagamento_id'],m['pep'],m['classe_custo'],m['value']) for m in bundle['matches']])
    db.executemany('INSERT INTO provenance VALUES (?,?,?,?)', [(n,s['sha256'],s['bytes'],s['rows']) for n,s in bundle['sources'].items()])
    db.executescript((ROOT/'sql/views.sql').read_text(encoding='utf-8'))
    peps = [dict(row) for row in db.execute('SELECT * FROM vw_eac ORDER BY pep')]
    totals = {k: sum(row[k] for row in peps) for k in peps[0] if k != 'pep'}
    alerts = []
    for p in peps:
        if not p['baseline'] and p['eac']:
            alerts.append({'pep':p['pep'], 'code':'SEM_BASELINE', 'text':'Custo/projeção sem baseline no escopo.'})
        elif p['variance'] > 0:
            alerts.append({'pep':p['pep'], 'code':'ACIMA_BASELINE', 'text':'EAC acima da baseline aprovada.'})
        if p['overdue_commitment']:
            alerts.append({'pep':p['pep'], 'code':'PREVISAO_VENCIDA', 'text':'Compromisso de custo com previsão vencida; confirmar reprogramação.'})
    controls=[]
    for c in bundle['controls']:
        actual, commitment = db.execute("SELECT COALESCE(SUM(CASE WHEN kind='REALIZADO' THEN value ELSE 0 END),0), COALESCE(SUM(CASE WHEN kind='COMPROMISSO' THEN value ELSE 0 END),0) FROM facts WHERE pep=? AND classe_custo=?",(c['pep'],c['classe_custo'])).fetchone()
        comparable=c['comparavel']=='SIM'
        row=dict(c,actual_model=actual,commitment_model=commitment,delta_actual=actual-c['actual_ref'] if comparable else None,delta_commitment=commitment-c['commitment_ref'] if comparable else None)
        controls.append(row)
        db.execute('INSERT INTO controls VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',(row['id'],row['fonte'],row['pep'],row['classe_custo'],row['actual_ref'],row['commitment_ref'],row['budget_ref'],row['remaining_plan_ref'],row['assigned_ref'],comparable,row['delta_actual'],row['delta_commitment'],json.dumps(row,ensure_ascii=False)))
        if comparable and (row['delta_actual'] or row['delta_commitment']):
            alerts.append({'pep':row['pep'],'code':'DIVERGENCIA_REFERENCIA','text':'Diferença frente ao total externo declarado comparável; investigar seleção, classificação e origem.'})
    report = {**bundle, 'controls':controls, 'version':VERSION, 'run_id':str(uuid4()), 'generated_at':datetime.now(timezone.utc).isoformat(), 'totals':totals, 'pep_metrics':peps, 'monthly':[dict(r) for r in db.execute('SELECT * FROM vw_monthly ORDER BY period,pep,kind')], 'alerts':alerts}
    db.commit()
    return report, db
