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
