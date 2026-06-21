from fastapi import APIRouter
from fastapi import Depends
from middlewares.api_guard import require_admin, require_user
from repositories.analytic_repository import _get_arr, _get_mrr

analytic_router = APIRouter(prefix="/analytics", tags=["payments"])

@analytic_router.get("/revenue/mrr")
async def get_mrr(current_user=Depends(require_user)):
    return await _get_mrr(current_user["user_id"])

@analytic_router.get("/revenue/arr")
async def get_arr(current_user=Depends(require_user)):
    return await _get_arr(current_user["user_id"])



    