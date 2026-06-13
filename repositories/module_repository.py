from core.database import client
from schemas.module_schema import Module
from commons.response import GenericResponse

db = client.get_default_database()
collection = db["modules"]

async def upsert_module(data: Module):
    await collection.update_one(
        {"name": data.name},
        {"$set": data.model_dump()},
        upsert=True
    )
    return GenericResponse(success=True, message="Module upserted successfully")
    
async def get_all_modules_by_user(user_id: str):
    modules = await collection.find(
        {"user_id": user_id},
        {"_id": 0}
    ).to_list(length=None)

    return GenericResponse(
        success=True,
        message="Modules retrieved successfully",
        data=modules
    )