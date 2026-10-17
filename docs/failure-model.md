# CommitBoundary Failure Model

## 1. Purpose

CommitBoundary is a reproducible test harness for investigating how AI agents behave when state-changing tool actions have ambiguous outcomes.

The initial scenario simulates a refund that commits successfully, but whose response is lost due to a timeout. The agent or caller then retries the same request.

The environment is simulated. It does not process real refunds or prevent real-world side effects.

## 2. System Under Test

The current implementation contains:

- `RefundSimulator`: maintains an in-memory refund total and processed-request records.
- `TimeoutAfterCommit`: injects a deterministic, one-shot timeout.
- `RefundTool`: invokes the simulator and then injects the timeout.
- Pytest tests: verify input validation, idempotency behavior, and recovery after a simulated timeout.

## 3. Modeled Failure

### Commit followed by response loss

1. A valid refund request reaches the simulator.
2. The simulator updates its refund total and records the request result.
3. The fault injector triggers a timeout before the result reaches the caller.
4. The caller retries using the same request ID and amount.
5. The simulator returns the original result without applying the refund again.

This models an ambiguous outcome: the caller observes a timeout, but the operation has already committed.

## 4. Current Guarantees

Within the current single-process, in-memory simulator:

- Refund amounts must be positive integers.
- Boolean amounts are rejected.
- Request IDs must be non-empty strings.
- Reusing a request ID with a different amount raises `ValueError`.
- Repeating a valid request with the same ID and amount returns its original result.
- A duplicate retry does not increase the refund total.
- The timeout fault triggers once per fault-injector instance.
- Importing `refund.py` does not execute its demonstration operations.

These guarantees are verified by the current pytest suite.

## 5. Current Limitations

The implementation does not yet guarantee:

- Atomic handling of concurrent requests.
- Durable request records across process restarts.
- Recovery after a crash between updating the refund total and recording the request.
- Distributed idempotency across multiple processes or machines.
- Exactly-once execution of external side effects.
- Detection of every possible failure mode in an AI agent or tool integration.
- Prevention of real-world duplicate actions.

The in-memory dictionary is not a durable ledger. The current simulator is intended for controlled testing, not production financial processing.

## 6. Fault-Injection Scope

The current fault injector models a single timeout after the simulator has committed the operation.

It does not yet model:

- Timeouts before execution.
- Partial operations.
- Process crashes.
- Concurrent retries.
- Delayed or duplicated responses.
- Network partitions.
- Failures during persistence.

Additional fault types may be introduced as separate, deterministic scenarios.

## 7. Next Engineering Milestones

1. Introduce an explicit operation ledger.
2. Add invariant checks for duplicate side effects and state consistency.
3. Build a deterministic scenario runner.
4. Capture structured execution traces and metrics.
5. Expand fault scenarios and benchmark methodology.

Each new guarantee must have a corresponding regression test and must be described according to the evidence collected.

## 8. Claims and Terminology

CommitBoundary currently tests and diagnoses behavior in a simulated environment. It does not claim universal prevention of duplicate side effects or guaranteed exactly-once execution.

Benchmark results must identify the tested scenario, assumptions, observed outcomes, and limitations.
