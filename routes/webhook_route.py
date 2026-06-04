from fastapi import APIRouter, Request
from core.logging import logger
from schemas.customer_schema import Customer
from schemas.cart_schema import Cart
from schemas.card_schema import Card
from commons.enums import SubscriptionEvent, PaymentEvent
from schemas.subscription_schema import Subscription
from schemas.payment_schema import Payment
from repositories.subscription_repository import upsert_subscription
from repositories.payment_repository import upsert_payment

webhook_router = APIRouter()

@webhook_router.post("/webhook/payment")
async def payment_webhook(req: Request):
    body = await req.json()
    event_type = body["type"]

    print(f"Received webhook event: {event_type}")
    
    if event_type in PaymentEvent:
        wh_response = Payment(
            business_id=body["business_id"],
            payment_id=body["data"]["payment_id"],
            event_type=event_type,
            created_at=body["data"]["created_at"],
            currency=body["data"]["currency"],
            status=body["data"]["status"],
            total_amount=body["data"]["total_amount"],
            invoice_id=body["data"]["invoice_id"],
            invoice_url=body["data"]["invoice_url"],
            cart=Cart(
                product_id=body["data"]["product_cart"][0]["product_id"],
                quantity=body["data"]["product_cart"][0]["quantity"]
            ),
            card=Card(
                card_holder_name=body["data"]["card_holder_name"],
                card_issuing_country=body["data"]["card_issuing_country"],
                card_last_four=body["data"]["card_last_four"],
                card_network=body["data"]["card_network"],
                card_type=body["data"]["card_type"]
            ),
            customer=Customer(
                customer_id=body["data"]["customer"]["customer_id"],
                email=body["data"]["customer"]["email"],
                name=body["data"]["customer"]["name"],
                phone_number=body["data"]["customer"]["phone_number"]
            )
        )

        await upsert_payment(wh_response)

        logger.info(
            "Business=%s Event=%s Payment ID=%s",
            wh_response.business_id,
            wh_response.event_type,
            wh_response.payment_id
        )

        return {"data": wh_response}
    else:
        return {"data": "Event type not handled"}
    
@webhook_router.post("/webhook/subscription")
async def subscription_webhook(req: Request):
    body = await req.json()
    event_type = body["type"]
    
    print(f"Received webhook event: {event_type}")
    
    if event_type in SubscriptionEvent:
        wh_response = Subscription(
            business_id=body["business_id"],
            event_type=event_type,
            created_at=body["data"]["created_at"],
            currency=body["data"]["currency"],
            status=body["data"]["status"],
            subscription_id=body["data"]["subscription_id"],
            product_id=body["data"]["product_id"],
            customer=Customer(
                customer_id=body["data"]["customer"]["customer_id"],
                email=body["data"]["customer"]["email"],
                name=body["data"]["customer"]["name"],
                phone_number=body["data"]["customer"]["phone_number"]
            )
        )

        await upsert_subscription(wh_response)

        logger.info(
            "Business=%s Event=%s Subscription ID=%s",
            wh_response.business_id,
            wh_response.event_type,
            wh_response.subscription_id
        )

        return {"data": wh_response}
    else:
        return {"data": "Event type not handled"}