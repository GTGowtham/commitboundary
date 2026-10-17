"""Refund function tests."""
import pytest
import refund

@pytest.fixture

def clean_refund_state():
    # Reset refunded_amount to zero
    refund.refunded_amount=0

def test_refund_amount(clean_refund_state):
    result=refund.refund(500)
    assert result == 500
    print("Test passed")

def test_multiple_refund(clean_refund_state):
    
    # Call refund with 500 and 200 save the result
    result1=refund.refund(500)
    result2=refund.refund(200)
    
    #Assert the first result is 500 and second result 700
    assert result1==500
    assert result2==700


def test_import_does_not_execute_refund_demo():
    import subprocess
    import sys

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import refund; print(refund.refunded_amount)",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.stdout.strip() == "0"

