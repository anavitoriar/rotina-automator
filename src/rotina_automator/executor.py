from __future__ import annotations

from typing import Tuple
from .planner import PlannedAction


def run_plan(plan: list[PlannedAction], dry_run: bool) -> Tuple[int, list[str]]:
    """
    Retorna:
      applied: quantas ações foram aplicadas (0 em dry-run)
      errors: lista de erros ocorridos na execução
    """
    errors: list[str] = []

    if not plan:
        print("No actions planned.")
        return 0, errors

    print("\nPLAN:")
    for item in plan:
        print(f"{item.type}: {item.src} -> {item.dst}")

    if dry_run:
        print("\nNo changes applied (dry-run).")
        return 0, errors

    # Amanhã a gente implementa execução de verdade
    print("\nExecution not implemented yet (placeholder).")
    return 0, errors
