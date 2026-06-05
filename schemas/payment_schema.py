from pydantic import BaseModel
from typing import Optional
from schemas.customer_schema import Customer
from schemas.card_schema import Card
from schemas.cart_schema import Cart

class Payment(BaseModel):
    payment_id: str 
    subscription_id: str
    invoice_id: str
    invoice_url: str
    business_id: str
    event_type: str
    created_at: str    
    total_amount: float
    currency: str
    status: str
    cart: Optional[Cart] = None 
    card: Card
    customer: Customer