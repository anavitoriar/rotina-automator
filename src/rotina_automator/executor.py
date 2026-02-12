from __future__ import annotations

import shutil
from pathlib import Path
from typing import Tuple

from .planner import PlannedAction


def run_plan(plan: list[PlannedAction], dry_run: bool) -> Tuple[int, list[str]]:
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

    applied = 0

    for item in plan:
        try:
            if item.type == "MOVE":
                src = Path(item.src)
                dst = Path(item.dst)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                applied += 1

            elif item.type == "RENAME":
                src = Path(item.src)
                dst = Path(item.dst)
                src.rename(dst)
                applied += 1

            else:
                errors.append(f"Unsupported action type: {item.type}")

        except Exception as e:
            errors.append(f"{item.type} failed: {item.src} -> {item.dst} ({e})")

    return applied, errors
