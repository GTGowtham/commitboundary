import pytest 
from tool_wrapper import RefundTool

def test_timeout_after_commit_then_retry():
      tool=RefundTool()
      
       # First call commits the refund but loses the response.
      with pytest.raises(TimeoutError):
            tool.refund(500,"refund-001")
      
      # The action committed despite the timeout.
      assert tool.simulator.refund_amount ==500
      
      # Retrying the same request must not duplicate the refund
      result=tool.refund(500,"refund-001")
      assert result ==500
      assert tool.simulator.refund_amount==500
      assert len(tool.simulator.processed_request) == 1


def test_wrapper_rejects_conflicting_retry():
    tool = RefundTool()

    # First request commits successfully after the initial timeout.
    with pytest.raises(TimeoutError):
        tool.refund(500, "refund-001")

    # Retry with the same ID but a different amount must fail.
    with pytest.raises(ValueError):
        tool.refund(900, "refund-001")

    # Neither the total nor the request history should change.
    assert tool.simulator.refund_amount == 500
    assert len(tool.simulator.processed_request) == 1
