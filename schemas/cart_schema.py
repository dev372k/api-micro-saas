from pydantic import BaseModel
from typing import Optional

class Cart(BaseModel):
    product_id: str
    quantity: int