from core.config import settings
from commons.constant import PRODUCTS
from commons.response import GenericResponse
from dodopayments import DodoPayments

client = DodoPayments(
    bearer_token=settings.DODO_API_KEY,
    environment=settings.DODO_ENVIRONMENT,  # defaults to "live_mode"
)

async def create_checkout_session(email: str, name: str, product_id: str) -> GenericResponse:
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
        return_url=settings.FE_BASE_URL,
    )

    return GenericResponse(success=True, message="Checkout session created successfully", data={"checkout_url": session.checkout_url})

async def preview_change_plan(subscription_id: str, new_product_id: str):
    preview = client.subscriptions.preview_change_plan(
        subscription_id=subscription_id,
        product_id=new_product_id,
        quantity=1,
        proration_billing_mode="difference_immediately"
    )

    return GenericResponse(success=True, message="Plan preview generated successfully", data={"preview": preview})

async def change_plan(subscription_id: str, new_product_id: str):
    result = client.subscriptions.change_plan(
        subscription_id=subscription_id,
        product_id=new_product_id,
        quantity=1,
        proration_billing_mode="difference_immediately",
        on_payment_failure="prevent_change",  # Optional: control behavior on payment failure
    )
    
    return GenericResponse(success=True, message="Plan changed successfully", data={"result": result})
