from pydantic import BaseModel
from typing import Optional

class Card(BaseModel):
    card_holder_name: str
    card_issuing_country: str
    card_last_four: str
    card_network: str
    card_type: str