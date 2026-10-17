class refundSimulator:
      def __init__(self):
            self.refund_amount=0
            self.processed_request={}
            

      def refund(self,incoming_amount,request_id):
            if request_id in self.processed_request:
                  if self.processed_request[request_id] != incoming_amount:
                        raise ValueError("Request ID reused with a different amount")
                  else:
                        return self.processed_request[request_id]
            self.refund_amount = incoming_amount + self.refund_amount
            self.processed_request[request_id] = incoming_amount
            return self.refund_amount

r1=refundSimulator()
r2=refundSimulator()
print(r1.refund(500,"refund-001"))
print(r1.refund(500, "refund-001"))
print(r2.refund(200,"refund-002"))