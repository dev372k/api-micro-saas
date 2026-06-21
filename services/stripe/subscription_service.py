from services.stripe.stripe_client import StripeClient

class SubscriptionService:

    def __init__(self, stripe_client:StripeClient):
        self.client = stripe_client.client

    def active_subscriptions(self):

        count = 0

        subscriptions = self.client.subscriptions.list(
            status="active",
            limit=100
        )

        for _ in subscriptions.auto_paging_iter():
            count += 1

        return count

    def cancelled_subscriptions(self):

        count = 0

        subscriptions = self.client.subscriptions.list(
            status="canceled",
            limit=100
        )

        for _ in subscriptions.auto_paging_iter():
            count += 1

        return count