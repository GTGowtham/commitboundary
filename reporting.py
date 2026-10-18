
import json
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scenario_runner import ScenarioResult


def build_report(
    result: "ScenarioResult",
    scenario_name: str,
) -> dict:
    return {
        "scenario_name": scenario_name,
        "status": "passed",
        "final_total": result.final_total,
        "final_history_entries": result.final_history_entries,
        "steps": [asdict(step) for step in result.trace],
    }


def write_report(report: dict, output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
