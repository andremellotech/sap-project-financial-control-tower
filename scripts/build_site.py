"""Build only the fictitious demo and its legacy routes, without modifying sources."""
import argparse
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Explicit publication allowlist: never copy a repository tree or local reports.
PUBLIC_FILES = (
    'index.html',
    'reports/demo/index.html',
    'reports/demo/relatorio.json',
    'reports/demo/finance.sqlite',
    'reports/demo/fatos.csv',
    'reports/demo/peps.csv',
    'reports/demo/conciliacoes.csv',
    'reports/demo/conferencia.csv',
)


def generate(stage):
    from finance.engine import calculate
    from finance.loader import load_bundle
    from finance.export import write_report, render
    report, db = calculate(load_bundle(ROOT/'sample-input', ROOT/'config/manifest.json'))
    try:
        write_report(report, db, stage/'reports/demo')
        (stage/'index.html').write_text(render(report, './reports/demo/'), encoding='utf-8')
    finally:
        db.close()


def build_site(output):
    target = Path(output).resolve()
    if target.exists():
        raise ValueError('A saída já existe; escolha uma pasta nova. Arquivos existentes preservados.')
    if target == ROOT or target in ROOT.parents or any(
        target.is_relative_to(ROOT/name) for name in ('sample-input', 'starter', 'config', 'web', 'docs', 'tests', 'scripts', 'reports', 'examples', '.git')
    ):
        raise ValueError('Escolha uma saída separada das fontes, por exemplo dist/.')
    with tempfile.TemporaryDirectory(prefix='portfolio-demo-') as temporary:
        stage = Path(temporary)
        generate(stage)
        # Check the complete artifact before creating the destination.
        sources = {relative: (ROOT/relative if relative.startswith(('docs/', 'starter/')) else stage/relative) for relative in PUBLIC_FILES}
        for relative, source in sources.items():
            if not source.is_file():
                raise FileNotFoundError(relative)
        target.mkdir(parents=True)
        for relative, source in sources.items():
            destination = target/relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
        (target/'.nojekyll').touch()
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerar demonstração fictícia completa para publicação ou uso offline.')
    parser.add_argument('--output', type=Path, default=ROOT/'dist')
    args = parser.parse_args()
    try:
        target = build_site(args.output)
    except (ValueError, OSError) as exc:
        parser.exit(1, str(exc)+'\n')
    print('Demonstração gerada em '+str(target/'index.html'))
