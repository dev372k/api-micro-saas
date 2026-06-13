from pydantic import BaseModel
from typing import Optional

class Card(BaseModel):
    card_holder_name: Optional[str] = None
    card_issuing_country: Optional[str] = None
    card_last_four: Optional[str] = None
    card_network: Optional[str] = None
    card_type: Optional[str] = None 