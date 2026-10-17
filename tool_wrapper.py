import faults
import simulator
from simulator import refundSimulator
from faults import timeoutAfterCommit

class RefundTool:
      def __init__(self):
            self.simulator=refundSimulator()
            self.faults=timeoutAfterCommit()
      
      
      def refund(self, amount, request_id):
            result = self.simulator.refund(amount, request_id)

            if self.faults.should_timeout():
                  raise TimeoutError("Response lost after refund committed")

            return result


# r1 = RefundTool()

# try:
#     print(r1.refund(500, "refund-001"))
# except TimeoutError as error:
#     print(f"First attempt timed out: {error}")

# print("Refund total after timeout:", r1.simulator.refund_amount)

# print("Retry result:", r1.refund(500, "refund-001"))
# print("Final refund total:", r1.simulator.refund_amount)





         


