import argparse
from pathlib import Path

from .planner import build_plan
from .executor import run_plan
from .reports import write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="rotina-automator",
        description="Automatiza organização e renomeação de arquivos com modo dry-run e relatório.",
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Pasta alvo onde as ações serão executadas.",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["organize", "rename"],
        help="Ação a executar: organize (mover por extensão) ou rename (renomear por regra).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria feito sem aplicar mudanças.",
    )
    parser.add_argument(
        "--report",
        default="report.json",
        help="Caminho do arquivo de relatório (JSON). Padrão: report.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target_path = Path(args.path).expanduser().resolve()

    plan, errors = build_plan(action=args.action, target_path=target_path)

    applied, exec_errors = run_plan(plan=plan, dry_run=args.dry_run)

    all_errors = errors + exec_errors
    report_path = Path(args.report).expanduser().resolve()

    write_report(
        report_path=report_path,
        action=args.action,
        target_path=str(target_path),
        dry_run=args.dry_run,
        plan=plan,
        applied=applied,
        errors=all_errors,
    )

    print(f"\nReport saved to: {report_path}")
    if all_errors:
        print(f"Completed with {len(all_errors)} error(s).")
    else:
        print("Completed successfully.")


if __name__ == "__main__":
    main()
