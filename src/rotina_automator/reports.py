from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .planner import PlannedAction


def write_report(
    report_path: Path,
    action: str,
    target_path: str,
    dry_run: bool,
    plan: list[PlannedAction],
    applied: int,
    errors: list[str],
) -> None:
    data = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "path": target_path,
        "dry_run": dry_run,
        "summary": {
            "planned": len(plan),
            "applied": applied,
            "errors": len(errors),
        },
        "items": [
            {
                "type": p.type,
                "src": p.src,
                "dst": p.dst,
                "status": "PLANNED" if dry_run else "PENDING",
            }
            for p in plan
        ],
        "errors": errors,
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
