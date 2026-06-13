from pydantic import BaseModel
from typing import Optional

class UserRequest(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    password: str