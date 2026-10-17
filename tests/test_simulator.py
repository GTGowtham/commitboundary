import pytest
from simulator import RefundSimulator


def test_multiple_refund():
    r1 = RefundSimulator()
    r2 = RefundSimulator()

    assert r1.refund(500, "refund-001") == 500
    assert r2.refund(200, "refund-002") == 200


def test_duplicate_refund():
    r1 = RefundSimulator()

    assert r1.refund(500, "refund-001") == 500
    assert r1.refund(500, "refund-001") == 500
    assert r1.refund_amount == 500


def test_conflicting_request_id():
    r1 = RefundSimulator()
    r1.refund(500, "refund-001")

    with pytest.raises(ValueError):
        r1.refund(900, "refund-001")

    assert r1.refund_amount == 500


def test_retry_returns_original_result_after_another_refund():
    simulator = RefundSimulator()

    # Request A commits.
    assert simulator.refund(500, "refund-A") == 500

    # Request B changes the current total.
    assert simulator.refund(200, "refund-B") == 700

    # Retrying A must return A's original result.
    assert simulator.refund(500, "refund-A") == 500

    # The retry must not create another side effect.
    assert simulator.refund_amount == 700


@pytest.mark.parametrize("amount", [0, -100])
def test_reject_non_positive_amount(amount):
    simulator = RefundSimulator()

    with pytest.raises(ValueError):
        simulator.refund(amount, "refund-001")

    assert simulator.refund_amount == 0
    assert simulator.processed_request == {}


@pytest.mark.parametrize("amount", [True, 500.5, "500", None])
def test_reject_invalid_amount_type(amount):
    simulator = RefundSimulator()

    with pytest.raises(TypeError):
        simulator.refund(amount, "refund-001")

    assert simulator.refund_amount == 0
    assert simulator.processed_request == {}


@pytest.mark.parametrize("request_id", ["", "   "])
def test_reject_blank_request_id(request_id):
    simulator = RefundSimulator()

    with pytest.raises(ValueError):
        simulator.refund(500, request_id)

    assert simulator.refund_amount == 0
    assert simulator.processed_request == {}


@pytest.mark.parametrize("request_id", [None, 123, True])
def test_reject_invalid_request_id_type(request_id):
    simulator = RefundSimulator()

    with pytest.raises(TypeError):
        simulator.refund(500, request_id)

    assert simulator.refund_amount == 0
    assert simulator.processed_request == {}
