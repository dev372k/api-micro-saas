from pydantic import BaseModel
from typing import Optional

class Customer(BaseModel):
    customer_id: str
    email: str
    name: str
    phone_number: Optional[str] = None