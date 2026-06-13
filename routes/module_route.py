from fastapi import APIRouter
from fastapi import Depends
from schemas.module_schema import Module
from models.module_request import ModuleRequest
from middlewares.api_guard import require_admin, require_user
from repositories.module_repository import get_all_modules_by_user, upsert_module

module_router = APIRouter(prefix="/modules", tags=["modules"])

@module_router.get("/")
async def get_modules(current_user=Depends(require_user)):
    return await get_all_modules_by_user(current_user["user_id"])

@module_router.post("/")
async def create_module(req:ModuleRequest, current_user=Depends(require_user)):
    return await upsert_module(Module(name=req.name, key=req.key, user_id=current_user["user_id"]))
    