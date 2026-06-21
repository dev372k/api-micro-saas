import stripe

class StripeClient:
    def __init__(self, api_key: str):
        self.client = stripe.StripeClient(api_key)