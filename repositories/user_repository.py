from core.database import client
from schemas.user_schema import User
from models.user_request import UserRequest
from models.login_request import LoginRequest
from commons.response import GenericResponse
from commons.security import Security

db = client.get_default_database()
collection = db["users"]

class UserRepository:
    @staticmethod
    async def create_user(req: UserRequest) -> User:
        existing_user = await collection.find_one({"email": req.email})
        if not existing_user:
            user = User(
                name=req.name,
                email=req.email,
                phone_number=req.phone_number,
                password_hash=Security.hash_password(req.password),
                role='user'
            )
            result = await collection.insert_one(user.model_dump())
            return GenericResponse(success=True, message="User created successfully", data={
                                       "_id": str(result.inserted_id), 
                                       "email": user.email, 
                                       "name": user.name, 
                                       "role": user.role
                                       }
                                    )
        else:
            return GenericResponse(success=False, message="User already exists", data=[])
        
    @staticmethod
    async def login(req: LoginRequest) -> User:
        existing_user = await collection.find_one({"email": req.email})
        if not existing_user:
            return GenericResponse(success=False, message="User not found", data=[])
        if Security.verify_password(req.password, existing_user["password_hash"]):
            return GenericResponse(success=True, message="Login successful", data=Security.create_access_token({
                    "user_id": str(existing_user["_id"]), 
                    "email": existing_user["email"], 
                    "name": existing_user["name"],
                    "role": existing_user["role"]}
                ))
        else:
            return GenericResponse(success=False, message="Invalid credentials", data=[])
    