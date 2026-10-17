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