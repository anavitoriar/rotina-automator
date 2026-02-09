from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


ActionType = Literal["MOVE", "RENAME"]


@dataclass(frozen=True)
class PlannedAction:
    type: ActionType
    src: str
    dst: str


def build_plan(action: str, target_path: Path) -> tuple[list[PlannedAction], list[str]]:
    errors: list[str] = []
    plan: list[PlannedAction] = []

    if not target_path.exists():
        return [], [f"Path does not exist: {target_path}"]
    if not target_path.is_dir():
        return [], [f"Path is not a directory: {target_path}"]

    # Hoje: só validar e retornar vazio (implementamos organize/rename amanhã e quarta)
    return plan, errors
