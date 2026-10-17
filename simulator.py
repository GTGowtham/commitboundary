
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefundRecord:
    amount: int
    result: int


class refundSimulator:
    def __init__(self):
        self.refund_amount = 0
        self.processed_request: dict[str, RefundRecord] = {}

    def refund(self, incoming_amount: int, request_id: str) -> int:
        # 1. Check whether this request was already processed.
        if request_id in self.processed_request:
            record = self.processed_request[request_id]

            # 2. Reject reuse of the same ID with a different amount.
            if record.amount != incoming_amount:
                raise ValueError(
                    "Request ID reused with a different amount"
                )

            # 3. Return the original result, not the current total.
            return record.result

        # 4. Process a new request.
        self.refund_amount += incoming_amount
        result = self.refund_amount

        # 5. Save both the original amount and original result.
        self.processed_request[request_id] = RefundRecord(
            amount=incoming_amount,
            result=result,
        )

        return result



if __name__ == "__main__":
      r1=refundSimulator()
      r2=refundSimulator()
      print(r1.refund(500,"refund-001"))
      print(r1.refund(500, "refund-001"))
      print(r2.refund(200,"refund-002"))
   
    