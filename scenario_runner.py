
from dataclasses import dataclass

from tool_wrapper import RefundTool
from reporting import build_report, write_report

@dataclass(frozen=True)
class ScenarioStep:
    amount: int
    request_id: str
    expected_result: int | None = None
    expected_exception: type[Exception] | None = None


@dataclass(frozen=True)
class StepObservation:
    step_number: int
    request_id: str
    outcome: str
    result: int | None
    total_after_step: int
    history_entries: int


@dataclass(frozen=True)
class ScenarioResult:
    trace: tuple[StepObservation, ...]
    final_total: int
    final_history_entries: int


def run_scenario(steps: list[ScenarioStep]) -> ScenarioResult:
    # A fresh tool gives every run an independent starting state.
    tool = RefundTool()
    observations = []

    for step_number, step in enumerate(steps, start=1):
        try:
            result = tool.refund(step.amount, step.request_id)

        except Exception as exc:
            if step.expected_exception is None:
                raise AssertionError(
                    f"Step {step_number}: unexpected "
                    f"{type(exc).__name__}: {exc}"
                ) from exc

            if type(exc) is not step.expected_exception:
                raise AssertionError(
                    f"Step {step_number}: expected "
                    f"{step.expected_exception.__name__}, got "
                    f"{type(exc).__name__}"
                ) from exc

            outcome = f"exception:{type(exc).__name__}"
            result = None

        else:
            if step.expected_exception is not None:
                raise AssertionError(
                    f"Step {step_number}: expected "
                    f"{step.expected_exception.__name__}, "
                    "but the call succeeded"
                )

            if (
                step.expected_result is not None
                and result != step.expected_result
            ):
                raise AssertionError(
                    f"Step {step_number}: expected result "
                    f"{step.expected_result}, got {result}"
                )

            outcome = "success"

        observations.append(
            StepObservation(
                step_number=step_number,
                request_id=step.request_id,
                outcome=outcome,
                result=result,
                total_after_step=tool.simulator.refund_amount,
                history_entries=len(
                    tool.simulator.processed_request
                ),
            )
        )

    return ScenarioResult(
        trace=tuple(observations),
        final_total=tool.simulator.refund_amount,
        final_history_entries=len(
            tool.simulator.processed_request
        ),
)
if __name__ == "__main__":
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
    write_report(report, "reports/scenario_report.json")

    print("Scenario:", report["scenario_name"])
    print("Status:", report["status"])
    print("Final total:", result.final_total)
    print("Final history entries:", result.final_history_entries)
    print("Report saved to: reports/scenario_report.json")
