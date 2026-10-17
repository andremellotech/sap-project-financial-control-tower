import copy
import csv
import json
from pathlib import Path
import tempfile
import unittest

from finance.loader import load_bundle, ValidationError
from finance.engine import calculate

ROOT = Path(__file__).resolve().parents[1]


class FinanceTests(unittest.TestCase):
    def test_portfolio_has_four_projects_and_distinct_financial_scenarios(self):
        report, db = calculate(self.load())
        try:
            self.assertEqual({p['projeto'] for p in report['peps']}, {'AURORA','HORIZONTE','ATLAS','VERTICE'})
            self.assertEqual(len(report['pep_metrics']), 22)
            expected = {'AURORA':(100_000_000,48_000_000,105_000_000),
                        'HORIZONTE':(240_000_000,85_000_000,232_000_000),
                        'ATLAS':(160_000_000,113_000_000,182_000_000),
                        'VERTICE':(80_000_000,69_000_000,76_000_000)}
            for project, amounts in expected.items():
                leaves={p['pep'] for p in report['peps'] if p['projeto']==project and p['leaf']}
                rows=[p for p in report['pep_metrics'] if p['pep'] in leaves]
                self.assertEqual(tuple(sum(p[k] for p in rows) for k in ('baseline','actual','eac')),amounts)
        finally:
            db.close()

    def load(self):
        return load_bundle(ROOT/'sample-input', ROOT/'config/manifest.json')

    def mutate(self, filename, fn):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        dest = Path(temp.name)
        for p in (ROOT/'sample-input').glob('*.csv'):
            (dest/p.name).write_bytes(p.read_bytes())
        path = dest/filename
        with path.open(encoding='utf-8', newline='') as stream:
            reader = csv.DictReader(stream, delimiter=';')
            headers = reader.fieldnames
            rows = list(reader)
        fn(rows)
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=headers, delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
        return dest

    def test_totals_cost_cash_and_eac_are_distinct(self):
        report, _ = calculate(self.load())
        k = report['totals']
        self.assertEqual(k['baseline'], 580_000_000)
        self.assertEqual(k['baseline_cut'], 471_000_000)
        self.assertEqual(k['actual'], 315_000_000)
        self.assertEqual(k['commitment'], 162_000_000)
        self.assertEqual(k['etc'], 118_000_000)
        self.assertEqual(k['eac'], 595_000_000)
        self.assertEqual(k['variance'], 15_000_000)
        self.assertEqual(k['paid'], 249_190_000)
        self.assertEqual(k['cash_commitment'], 106_000_000)
        self.assertEqual(k['matched'], 245_190_000)
        self.assertEqual(k['actual_unmatched'], 69_810_000)
        self.assertEqual(k['cash_unmatched'], 4_000_000)

    def test_parent_rows_do_not_double_count_leaf_postings(self):
        report, db = calculate(self.load())
        try:
            total = db.execute('select sum(actual) from vw_pep_finance').fetchone()[0]
            self.assertEqual(total, report['totals']['actual'])
            self.assertEqual(len(report['pep_metrics']), 22)
            self.assertEqual(len(report['peps']), 33)
        finally:
            db.close()

    def test_negative_credit_and_settlement_are_preserved(self):
        report, db = calculate(self.load())
        db.close()
        facts = {f['id']: f for f in report['facts']}
        self.assertEqual(facts['A04']['value'], -2_000_000)
        self.assertEqual(facts['S01']['kind'], 'LIQUIDACAO')
        self.assertEqual(report['totals']['settlement'], 10_000_000)

    def test_source_hash_and_physical_line_are_retained(self):
        bundle = self.load()
        self.assertEqual(len(bundle['sources']), 8)
        self.assertEqual(len(bundle['sources']['cji3.csv']['sha256']), 64)
        self.assertGreaterEqual(bundle['facts'][0]['source_line'], 2)

    def test_cost_on_parent_is_rejected(self):
        dest = self.mutate('cji3.csv', lambda rows: rows[0].update(pep='PRJ-01'))
        with self.assertRaisesRegex(ValidationError, 'folha'):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_cycle_is_rejected(self):
        dest = self.mutate('peps.csv', lambda rows: rows[0].update(pai='PRJ-01.01.01'))
        with self.assertRaisesRegex(ValidationError, 'ciclo'):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_future_actual_and_mixed_snapshot_rejected(self):
        for filename, column, value in [('cji3.csv','data','2026-10-01'),('cji5.csv','data_snapshot','2026-08-31')]:
            dest = self.mutate(filename, lambda rows: rows[0].update({column:value}))
            with self.assertRaises(ValidationError):
                load_bundle(dest, ROOT/'config/manifest.json')

    def test_wrong_baseline_version_and_duplicate_ids_rejected(self):
        dest = self.mutate('baseline.csv', lambda rows: rows[0].update(versao='BL-OUTRA'))
        with self.assertRaisesRegex(ValidationError, 'versão'):
            load_bundle(dest, ROOT/'config/manifest.json')
        dest = self.mutate('cji3.csv', lambda rows: rows.append(dict(rows[0])))
        with self.assertRaisesRegex(ValidationError, 'duplic'):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_overallocation_and_wrong_cash_kind_rejected(self):
        dest = self.mutate('conciliacoes.csv', lambda rows: rows[0].update(valor_brl='999999.00'))
        with self.assertRaisesRegex(ValidationError, 'aloca'):
            load_bundle(dest, ROOT/'config/manifest.json')
        dest = self.mutate('conciliacoes.csv', lambda rows: rows[0].update(pagamento_id='P05'))
        with self.assertRaises(ValidationError):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_unknown_pep_bad_decimal_and_non_future_etc_rejected(self):
        cases = [('cji3.csv','pep','NAO-EXISTE'), ('cji3.csv','valor_brl','NaN'), ('etc.csv','periodo','2026-09')]
        for filename, field, value in cases:
            dest = self.mutate(filename, lambda rows: rows[0].update({field:value}))
            with self.assertRaises(ValidationError):
                load_bundle(dest, ROOT/'config/manifest.json')

    def test_conflicting_natural_key_and_split_allocation(self):
        def duplicate(rows):
            extra = dict(rows[0]); extra['id'] = 'NOVO'; rows.append(extra)
        dest = self.mutate('cji5.csv', duplicate)
        with self.assertRaisesRegex(ValidationError, 'duplic'):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_manifest_cut_must_be_month_end(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'manifest.json'
            manifest = json.loads((ROOT/'config/manifest.json').read_text(encoding='utf-8'))
            manifest['data_corte'] = '2026-09-15'
            path.write_text(json.dumps(manifest), encoding='utf-8')
            with self.assertRaisesRegex(ValidationError, 'mês'):
                load_bundle(ROOT/'sample-input', path)

    def test_negative_payment_allocation_preserves_signed_net(self):
        dest = self.mutate('cjia.csv', lambda rows: rows.append(dict(rows[1], id='P06', documento='2000001006', valor_brl='-10000.00', data='2026-09-29')))
        path = dest/'conciliacoes.csv'
        with path.open('a', encoding='utf-8', newline='') as stream:
            stream.write('L05;A04;P06;-10000.00\n')
        report, db = calculate(load_bundle(dest, ROOT/'config/manifest.json'))
        db.close()
        self.assertEqual(report['totals']['paid'], 248_190_000)
        self.assertEqual(report['totals']['matched'], 244_190_000)
        self.assertEqual(report['totals']['cash_unmatched'], 4_000_000)
        self.assertEqual(report['totals']['eac'], 595_000_000)

    def test_cross_company_allocation_rejected(self):
        dest = self.mutate('cjia.csv', lambda rows: rows[0].update(empresa='2000'))
        with self.assertRaisesRegex(ValidationError, 'empresa'):
            load_bundle(dest, ROOT/'config/manifest.json')

    def test_empty_financial_snapshot_has_zero_totals(self):
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp)
            for p in (ROOT/'sample-input').glob('*.csv'):
                (dest/p.name).write_bytes(p.read_bytes() if p.name=='peps.csv' else p.read_bytes().splitlines(keepends=True)[0])
            report, db = calculate(load_bundle(dest, ROOT/'config/manifest.json'))
            db.close()
            self.assertTrue(all(v==0 for v in report['totals'].values()))

    def test_company_and_year_are_part_of_document_identity(self):
        def add(rows):
            rows.append(dict(rows[0], id='A08', empresa='2000', valor_brl='1.00'))
        dest = self.mutate('cji3.csv', add)
        report, db = calculate(load_bundle(dest, ROOT/'config/manifest.json'))
        db.close()
        self.assertEqual(report['totals']['actual'],315_000_100)

    def test_external_reference_is_independent_and_exposes_difference(self):
        report, db = calculate(self.load())
        db.close()
        row=next(c for c in report['controls'] if c['pep']=='PRJ-01.01.01')
        self.assertEqual(row['actual_ref'],9_500_000)
        self.assertEqual(row['delta_actual'],500_000)
        self.assertEqual(row['delta_commitment'],0)
        self.assertEqual(report['totals']['actual'],315_000_000)
        self.assertEqual(report['totals']['eac'],595_000_000)

    def test_noncomparable_reference_is_not_declared_reconciled(self):
        dest=self.mutate('conferencia_sap.csv',lambda rows:rows[0].update(comparavel='NAO'))
        report,db=calculate(load_bundle(dest,ROOT/'config/manifest.json'))
        db.close()
        self.assertIsNone(report['controls'][0]['delta_actual'])
        self.assertIsNone(report['controls'][0]['delta_commitment'])

    def test_reference_must_share_snapshot_and_use_leaf(self):
        for field,value in [('data_snapshot','2026-08-31'),('pep','PRJ-01'),('comparavel','TALVEZ')]:
            dest=self.mutate('conferencia_sap.csv',lambda rows:rows[0].update({field:value}))
            with self.assertRaises(ValidationError):
                load_bundle(dest,ROOT/'config/manifest.json')

    def test_missing_optional_reference_fields_are_null_not_zero(self):
        dest=self.mutate('conferencia_sap.csv',lambda rows:rows[0].update(orcamento_brl='',plan_re_brl='',disposto_brl=''))
        report,db=calculate(load_bundle(dest,ROOT/'config/manifest.json'))
        try:
            self.assertIsNone(report['controls'][0]['budget_ref'])
            self.assertIsNone(report['controls'][0]['remaining_plan_ref'])
            self.assertIsNone(report['controls'][0]['assigned_ref'])
            self.assertEqual(tuple(db.execute('select budget_ref,remaining_plan_ref,assigned_ref from controls where id="V01"').fetchone()),(None,None,None))
        finally:
            db.close()

    def test_duplicate_external_reference_is_rejected(self):
        def duplicate(rows):
            rows.append(dict(rows[0],id='V99'))
        dest=self.mutate('conferencia_sap.csv',duplicate)
        with self.assertRaisesRegex(ValidationError,'duplic'):
            load_bundle(dest,ROOT/'config/manifest.json')


if __name__ == '__main__':
    unittest.main()
