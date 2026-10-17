import pytest
from simulator import refundSimulator


def test_multiple_refund():
    r1 = refundSimulator()
    r2 = refundSimulator()

    assert r1.refund(500, "refund-001") == 500
    assert r2.refund(200, "refund-002") == 200


def test_duplicate_refund():
    r1 = refundSimulator()

    assert r1.refund(500, "refund-001") == 500
    assert r1.refund(500, "refund-001") == 500
    assert r1.refund_amount == 500


def test_conflicting_request_id():
    r1 = refundSimulator()
    r1.refund(500, "refund-001")

    with pytest.raises(ValueError):
        r1.refund(900, "refund-001")

    assert r1.refund_amount == 500


def test_retry_returns_original_result_after_another_refund():
    simulator = refundSimulator()

    # Request A commits.
    assert simulator.refund(500, "refund-A") == 500

    # Request B changes the current total.
    assert simulator.refund(200, "refund-B") == 700

    # Retrying A must return A's original result.
    assert simulator.refund(500, "refund-A") == 500

    # The retry must not create another side effect.
    assert simulator.refund_amount == 700
