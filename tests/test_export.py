import csv
import hashlib
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from finance.export import build
from finance.loader import ValidationError

ROOT = Path(__file__).resolve().parents[1]


class ExportTests(unittest.TestCase):
    def test_build_reproduces_sql_json_html_and_sources(self):
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'sample-input').glob('*')}
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'result'
            report = build(ROOT/'sample-input', ROOT/'config/manifest.json', output)
            self.assertEqual(json.loads((output/'relatorio.json').read_text(encoding='utf-8'))['totals'], report['totals'])
            db = sqlite3.connect(output/'finance.sqlite')
            try:
                self.assertEqual(db.execute('select sum(actual) from vw_eac').fetchone()[0], 315_000_000)
            finally:
                db.close()
            page = (output/'index.html').read_text(encoding='utf-8')
            self.assertNotIn('__DATA__', page)
            self.assertIn('"baseline":580000000', page)
            with (output/'fatos.csv').open(encoding='utf-8-sig', newline='') as stream:
                self.assertEqual(len(list(csv.DictReader(stream, delimiter=';'))), len(report['facts']))
        after = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'sample-input').glob('*')}
        self.assertEqual(before, after)

    def test_output_existing_and_inside_input_are_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)
            sentinel = output/'keep.txt'; sentinel.write_text('keep')
            with self.assertRaises(ValidationError):
                build(ROOT/'sample-input', ROOT/'config/manifest.json', output)
            self.assertEqual(sentinel.read_text(), 'keep')
        with self.assertRaises(ValidationError):
            build(ROOT/'sample-input', ROOT/'config/manifest.json', ROOT/'sample-input/result')

    def test_embedded_text_cannot_close_script_and_csv_formula_is_escaped(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp); source = folder/'input'; source.mkdir()
            for p in (ROOT/'sample-input').glob('*.csv'):
                (source/p.name).write_bytes(p.read_bytes())
            path = source/'cji3.csv'
            content = path.read_text(encoding='utf-8').replace('Projeto básico', '=HYPERLINK("x") </script><script>alert(1)</script>')
            path.write_text(content, encoding='utf-8')
            build(source, ROOT/'config/manifest.json', folder/'output')
            html = (folder/'output/index.html').read_text(encoding='utf-8')
            self.assertNotIn('</script><script>alert(1)', html)
            with (folder/'output/fatos.csv').open(encoding='utf-8-sig', newline='') as stream:
                rows = list(csv.DictReader(stream, delimiter=';'))
            self.assertTrue(next(r for r in rows if r['id']=='A01')['descricao'].startswith("'="))


if __name__ == '__main__':
    unittest.main()
