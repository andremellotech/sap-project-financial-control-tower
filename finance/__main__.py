import argparse
from pathlib import Path
import sys

from .engine import ROOT
from .export import build, demo
from .loader import ValidationError


def main():
    parser = argparse.ArgumentParser(description='Baseline, custo, compromissos e caixa por elemento PEP, via CSV normalizado.')
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('demo', help='Recriar a demonstração fictícia do pacote.')
    task = commands.add_parser('build', help='Validar entradas e gerar relatório em pasta nova.')
    task.add_argument('--input', type=Path, required=True)
    task.add_argument('--manifest', type=Path, default=ROOT/'config/manifest.json')
    task.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        report = demo() if args.command == 'demo' else build(args.input,args.manifest,args.output)
    except (ValidationError, OSError) as exc:
        print(f'Não foi possível gerar: {exc}',file=sys.stderr)
        return 1
    print(f"Relatório gerado | corte {report['manifest']['data_corte']} | {len(report['facts'])} fatos | {len(report['alerts'])} alertas gerenciais | execução {report['run_id']}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
