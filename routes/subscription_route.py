from fastapi import APIRouter, Depends
from external_services.payment_service import create_checkout_session
from middlewares.auth_v2 import require_user
from repositories.subscription_repository import get_all_subscriptions


subscription_router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@subscription_router.get("/")
async def get_subscriptions(current_user=Depends(require_user)):
    return await get_all_subscriptions()

@subscription_router.get("/generate-session/{product_id}")
async def generate_session(product_id: str = None, current_user=Depends(require_user)):
    return await create_checkout_session(email=current_user["email"], name=current_user["name"], product_id=product_id)
