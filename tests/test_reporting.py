
import json

from reporting import build_report, write_report
from scenario_runner import ScenarioStep, run_scenario


def test_report_contains_scenario_trace_and_final_state(tmp_path):
    scenario = [
        ScenarioStep(
            amount=500,
            request_id="refund-001",
            expected_exception=TimeoutError,
        ),
        ScenarioStep(
            amount=500,
            request_id="refund-001",
            expected_result=500,
        ),
    ]

    result = run_scenario(scenario)
    report = build_report(result, "timeout_then_retry")

    output_path = tmp_path / "scenario_report.json"
    write_report(report, output_path)

    saved_report = json.loads(output_path.read_text(encoding="utf-8"))

    assert saved_report["scenario_name"] == "timeout_then_retry"
    assert saved_report["status"] == "passed"
    assert saved_report["final_total"] == 500
    assert saved_report["final_history_entries"] == 1
    assert len(saved_report["steps"]) == 2
    assert saved_report["steps"][0]["outcome"] == "exception:TimeoutError"
    assert saved_report["steps"][1]["result"] == 500
