from fastapi import APIRouter

from models.login_request import LoginRequest
from models.user_request import UserRequest    
from repositories.user_repository import UserRepository
from models.user_request import UserRequest

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/auth")
async def auth(req: LoginRequest):
    return await UserRepository.login(req)

@user_router.post("/auth/google")
async def auth_google(req: UserRequest):
    return await UserRepository.login(req)  

@user_router.post("/register")
async def register(req: UserRequest):
    return await UserRepository.create_user(req)  