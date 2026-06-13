from fastapi import APIRouter
from fastapi import Depends
from middlewares.auth_v2 import require_admin, require_user
from repositories.payment_repository import get_all_payments_by_user

payment_router = APIRouter(prefix="/payments", tags=["payments"])

@payment_router.get("/")
async def get_payments(current_user=Depends(require_user)):
    return await get_all_payments_by_user(current_user["user_id"])
    