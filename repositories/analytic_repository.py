from core.database import client
from schemas.module_schema import Module
from commons.response import GenericResponse
from services.stripe.revenue_service import RevenueService
from services.stripe.stripe_client import StripeClient

db = client.get_default_database()
collection = db["modules"]
    
def revenue_service(key):
    stripe_client = StripeClient(key)
    return RevenueService(stripe_client)

async def get_key(user_id):
    module = await collection.find_one(
        {
            "user_id": user_id,
            "name": "stripe"
        },
        {
            "_id": 0
        }
    )
    if not module:
        return ""
    return module["key"]

async def _get_arr(user_id: str):
    key = get_key(user_id)

    if not key:
        return GenericResponse(
            success=False,
            message="Stripe module not found",
            data=None
        )

    arr = revenue_service(key).get_arr()

    return GenericResponse(
        success=True,
        message="Analytics retrieved successfully",
        data=arr
    )

async def _get_mrr(user_id: str):
    key = get_key(user_id)

    if not key:
        return GenericResponse(
            success=False,
            message="Stripe module not found",
            data=None
        )

    mrr = revenue_service(key).get_mrr()

    return GenericResponse(
        success=True,
        message="Analytics retrieved successfully",
        data=mrr
    )