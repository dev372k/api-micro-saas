from fastapi import APIRouter
from repositories.payment_repository import get_all_payments

payment_router = APIRouter(prefix="/payments", tags=["payments"])

@payment_router.get("/")
async def get_payments():
    return {
        "payments": await get_all_payments()
    }