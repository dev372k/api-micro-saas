from commons.response import GenericResponse
from core.database import client
from schemas.subscription_schema import Subscription

db = client.get_default_database()
collection = db["subscriptions"]

async def upsert_subscription(data: Subscription):
    await collection.update_one(
        {"subscription_id": data.subscription_id},
        {"$set": data.model_dump()},
        upsert=True
    )
    return GenericResponse(success=True, message="Subscription upserted successfully")

async def get_all_subscriptions():
    subscriptions = await collection.find({}, {"_id": 0}).to_list(length=None)
    return GenericResponse(success=True, message="Subscriptions retrieved successfully", data=subscriptions)
    