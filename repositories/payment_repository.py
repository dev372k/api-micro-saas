from core.database import client
from schemas.payment_schema import Payment
from commons.response import GenericResponse

db = client.get_default_database()
collection = db["payments"]

async def upsert_payment(data: Payment):
    await collection.update_one(
        {"payment_id": data.payment_id},
        {"$set": data.model_dump()},
        upsert=True
    )
    return GenericResponse(success=True, message="Payment upserted successfully")
    
async def get_all_payments_by_user(user_id):
    payments = await collection.find({"user_id": user_id}, {"_id": 0}).to_list(length=None)
    return GenericResponse(success=True, message="Payments retrieved successfully", data=payments)