from services.stripe.stripe_client import StripeClient

class RevenueService:

    def __init__(self, stripe_client: StripeClient):
        self.client = stripe_client.client

    def get_total_revenue(self):

        total = 0

        charges = self.client.charges.list(limit=100)

        for charge in charges.auto_paging_iter():
            if charge.paid:
                total += charge.amount

        return round(total / 100, 2)

    def get_mrr(self):

        mrr = 0

        subscriptions = self.client.subscriptions.list()

        for sub in subscriptions.auto_paging_iter():

            for item in sub["items"]["data"]:

                interval = item["price"]["recurring"]["interval"]

                amount = item["price"]["unit_amount"]

                quantity = item["quantity"]

                if interval == "month":
                    mrr += amount * quantity

                elif interval == "year":
                    mrr += (amount / 12) * quantity

        return round(mrr / 100, 2)

    def get_arr(self):
        return self.get_mrr() * 12