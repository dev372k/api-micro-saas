from fastapi import APIRouter, Request
from repositories.subscription_repository import get_all_subscriptions

subscription_router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@subscription_router.get("/")
async def get_subscriptions():
    return {
        "subscriptions": await get_all_subscriptions()
    }