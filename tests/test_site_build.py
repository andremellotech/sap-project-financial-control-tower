"""The static package preserves public demo routes and offline downloads."""
import json
import hashlib
import re
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

class SiteBuildTests(unittest.TestCase):
    def test_complete_offline_package_and_safe_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp)/'site'
            command = [sys.executable, '-X', 'utf8', '-B', str(ROOT/'scripts/build_site.py'), '--output', str(output)]
            before = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('sample-input', 'starter', 'config', 'web') if (ROOT/folder).exists() for p in (ROOT/folder).rglob('*') if p.is_file()}
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertTrue((output/'index.html').is_file())
            self.assertTrue((output/'.nojekyll').is_file())
            self.assertFalse((output/'web').exists())
            self.assertFalse((output/'sample-input').exists())
            self.assertFalse((output/'docs/images').exists())
            self.assertFalse((output/'tests').exists())
            for relative in EXPECTED:
                self.assertTrue((output/relative).is_file(), relative)
            verify_demo(self, output)
            for relative, digest in before.items():
                self.assertEqual(hashlib.sha256((ROOT/relative).read_bytes()).hexdigest(), digest, relative)
            class Links(HTMLParser):
                def handle_starttag(self, tag, attrs):
                    if tag in ('a', 'script', 'link', 'img'):
                        for key, value in attrs:
                            if key in ('href', 'src') and value:
                                parsed = urlsplit(value)
                                if not parsed.scheme and parsed.path:
                                    self_test.assertTrue((page.parent/unquote(parsed.path)).is_file(), str(page)+': '+value)
            self_test = self
            for page in output.rglob('*.html'):
                Links().feed(page.read_text(encoding='utf-8'))
            for document in output.rglob('*.md'):
                for link in re.findall(r'!?\[[^\]]*\]\(([^)\s]+)', document.read_text(encoding='utf-8')):
                    parsed = urlsplit(link)
                    if not parsed.scheme and parsed.path:
                        self.assertTrue((document.parent/unquote(parsed.path)).is_file(), str(document)+': '+link)
            sentinel = output/'keep.txt'
            sentinel.write_text('keep', encoding='utf-8')
            repeated = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            self.assertNotEqual(repeated.returncode, 0)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'keep')

EXPECTED = ['reports/demo/index.html', 'reports/demo/relatorio.json', 'reports/demo/finance.sqlite', 'reports/demo/fatos.csv', 'reports/demo/peps.csv', 'reports/demo/conciliacoes.csv', 'reports/demo/conferencia.csv']

def verify_demo(test, output):
    import sqlite3
    report = json.loads((output/'reports/demo/relatorio.json').read_text(encoding='utf-8'))
    test.assertEqual(report['totals']['actual'], 315000000)
    database = sqlite3.connect(output/'reports/demo/finance.sqlite')
    try:
        test.assertEqual(database.execute('SELECT sum(actual) FROM vw_eac').fetchone()[0], 315000000)
    finally:
        database.close()
    for page in ('index.html', 'reports/demo/index.html'):
        text = (output/page).read_text(encoding='utf-8')
        test.assertNotIn('<script src=', text)
        test.assertNotIn('__DATA__', text)
