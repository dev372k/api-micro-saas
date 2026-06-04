from core.database import client
from schemas.payment_schema import Payment

db = client.get_default_database()
collection = db["payments"]

async def upsert_payment(data: Payment):
    await collection.update_one(
        {"payment_id": data.payment_id},
        {"$set": data.model_dump()},
        upsert=True
    )
    
async def get_all_payments():
    return await collection.find({}, {"_id": 0}).to_list(length=None)