
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RefundRecord:
    amount: int
    result: int


class RefundSimulator:
    def __init__(self):
        self.refund_amount = 0
        self.processed_request: dict[str, RefundRecord] = {}

    def refund(self, incoming_amount: int, request_id: str) -> int:
        if type(incoming_amount) is not int:
            raise TypeError("Refund amount must be an integer")

        if incoming_amount <= 0:
            raise ValueError("Refund amount must be positive")

        if not isinstance(request_id, str):
            raise TypeError("Request ID must be a string")

        if not request_id.strip():
            raise ValueError("Request ID must not be empty")

        if request_id in self.processed_request:
            record = self.processed_request[request_id]

            if record.amount != incoming_amount:
                raise ValueError(
                    "Request ID reused with a different amount"
                )

            return record.result

        self.refund_amount += incoming_amount
        result = self.refund_amount

        self.processed_request[request_id] = RefundRecord(
            amount=incoming_amount,
            result=result,
        )

        return result


if __name__ == "__main__":
    r1 = RefundSimulator()
    r2 = RefundSimulator()

    print(r1.refund(500, "refund-001"))
    print(r1.refund(500, "refund-001"))
    print(r2.refund(200, "refund-002"))
