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

    if action == "organize":
        plan = build_organize_plan(target_path)
        return plan, errors

    if action == "rename":
        plan = build_rename_plan(target_path)
        return plan, errors


    return plan, errors


def build_organize_plan(target_path: Path) -> list[PlannedAction]:
    """
    Gera ações MOVE para organizar arquivos por extensão, criando pastas-alvo como:
    PDF/, IMG/, TXT/, OUTROS/, SEM_EXTENSAO/
    """
    ignore_dirs = {".git", ".venv", "__pycache__", "src", "tests"}
    plan: list[PlannedAction] = []

    def folder_for(ext: str) -> str:
        ext = ext.lower()
        if ext in {".pdf"}:
            return "PDF"
        if ext in {".png", ".jpg", ".jpeg", ".webp"}:
            return "IMG"
        if ext in {".txt"}:
            return "TXT"
        return "OUTROS"

    for item in target_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dirs:
                continue
            # Sprint 1 (MVP): não entra em subpastas
            continue

        ext = item.suffix
        if ext == "":
            dest_dir = target_path / "SEM_EXTENSAO"
        else:
            dest_dir = target_path / folder_for(ext)

        dest_path = dest_dir / item.name

        # evita criar ação "mover para o mesmo lugar"
        if dest_path.resolve() == item.resolve():
            continue

        plan.append(PlannedAction(type="MOVE", src=str(item), dst=str(dest_path)))

    return plan


import re


def slugify_filename(name: str) -> str:
    base = name.strip().lower()
    base = base.replace(" ", "_")
    base = re.sub(r"[^a-z0-9_.-]+", "", base)
    base = re.sub(r"_+", "_", base)
    base = base.strip("_")
    return base or "arquivo"


def resolve_collision(dst: Path) -> Path:
    """
    Se o destino já existir, cria sufixos: nome_1.ext, nome_2.ext...
    """
    if not dst.exists():
        return dst

    stem = dst.stem
    suffix = dst.suffix

    i = 1
    while True:
        candidate = dst.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def build_rename_plan(target_path: Path) -> list[PlannedAction]:
    ignore_dirs = {".git", ".venv", "__pycache__", "src", "tests"}
    plan: list[PlannedAction] = []

    for item in target_path.iterdir():
        if item.is_dir():
            if item.name in ignore_dirs:
                continue
            continue  # MVP: não entra em subpastas

        new_name = slugify_filename(item.name)
        if new_name == item.name:
            continue

        dst = item.with_name(new_name)
        dst = resolve_collision(dst)

        plan.append(PlannedAction(type="RENAME", src=str(item), dst=str(dst)))

    return plan
