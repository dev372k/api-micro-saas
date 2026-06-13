from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    phone_number: Optional[str] = None
    email: EmailStr
    password_hash: Optional[str] = Field(None)
    role: str
    is_active: Optional[bool] = Field(default=True)
    