from core.database import client
from schemas.subscription_schema import Subscription

db = client.get_default_database()
collection = db["payments"]

async def upsert_subscription(data: Subscription):
    await collection.update_one(
        {"subscription_id": data.subscription_id},
        {"$set": data.model_dump()},
        upsert=True
    )

async def get_all_subscriptions():
    return await collection.find({}, {"_id": 0}).to_list(length=None)
    