from pydantic import BaseModel

class SessionRequest(BaseModel):
    product_id: str
    name: str
    email: str