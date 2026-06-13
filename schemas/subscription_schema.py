from pydantic import BaseModel
from schemas.customer_schema import Customer

class Subscription(BaseModel):
    subscription_id: str
    business_id: str
    product_id: str
    event_type: str
    created_at: str    
    status: str
    currency: str
    customer: Customer