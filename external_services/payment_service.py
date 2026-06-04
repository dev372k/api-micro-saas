from core.config import settings
from commons.constant import PRODUCTS
from dodopayments import DodoPayments

client = DodoPayments(
    bearer_token=settings.DODO_PAYMENTS_API_KEY,
    environment="test_mode",  # defaults to "live_mode"
)

async def create_checkout_session(email: str, name: str, product_id: str) -> str:
    if product_id not in PRODUCTS.values():
        raise ValueError("Invalid product ID")
    
    session = client.checkout_sessions.create(
        product_cart=[
            {"product_id": product_id, "quantity": 1}
        ],
        # subscription_data={"trial_period_days": 14},  # optional
        customer={
            "email": email,
            "name": name,
        },
        return_url="https://quickvalide.com",
    )

    return session.checkout_url