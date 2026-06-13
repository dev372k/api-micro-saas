from stripe_client import StripeClient

class PaymentService:

    def __init__(self, stripe_client:StripeClient):
        self.client = stripe_client.client

    def successful_payments(self):

        count = 0

        charges = self.client.charges.list(limit=100)

        for charge in charges.auto_paging_iter():

            if charge.paid:
                count += 1

        return count

    def failed_payments(self):

        count = 0

        charges = self.client.charges.list(limit=100)

        for charge in charges.auto_paging_iter():

            if charge.status == "failed":
                count += 1

        return count

    def refunds(self):

        total = 0

        refunds = self.client.refunds.list(limit=100)

        for refund in refunds.auto_paging_iter():
            total += refund.amount

        return total / 100