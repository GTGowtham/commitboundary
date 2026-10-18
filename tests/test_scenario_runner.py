
from scenario_runner import ScenarioStep, run_scenario


def build_timeout_retry_scenario():
    return [
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


def test_same_scenario_produces_identical_traces():
    first = run_scenario(build_timeout_retry_scenario())
    second = run_scenario(build_timeout_retry_scenario())

    assert first == second
    assert first.final_total == 500
    assert first.final_history_entries == 1
    assert len(first.trace) == 2


def test_trace_records_commit_before_timeout_and_successful_retry():
    result = run_scenario(build_timeout_retry_scenario())

    timeout_step, retry_step = result.trace

    assert timeout_step.outcome == "exception:TimeoutError"
    assert timeout_step.total_after_step == 500
    assert timeout_step.history_entries == 1

    assert retry_step.outcome == "success"
    assert retry_step.result == 500
    assert retry_step.total_after_step == 500
    assert retry_step.history_entries == 1
