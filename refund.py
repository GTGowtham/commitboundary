"""Refund logic."""

refunded_amount=0
def refund(incoming_amount):
      # TODO 1: Declare that you want to modify the global variable.
      global refunded_amount
      # TODO 2: Add the incoming amount to the existing amount.
      refunded_amount=refunded_amount+incoming_amount
      # TODO 3: Return the updated total
      return refunded_amount

refund(500)
refund(200)
print(refunded_amount)