from fastapi import APIRouter
from external_services.payment_service import create_checkout_session
from repositories.subscription_repository import get_all_subscriptions
from models.session_request import SessionRequest

subscription_router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@subscription_router.get("/")
async def get_subscriptions():
    return {
        "subscriptions": await get_all_subscriptions()
    }

@subscription_router.post("/generate-session")
async def generate_session(req: SessionRequest):
    return {
        "checkout_url": await create_checkout_session(
            email=req.email,
            name=req.name,
            product_id=req.product_id
        )
    }