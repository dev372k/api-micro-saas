from pydantic import BaseModel

class OptimizeRequest(BaseModel):
    text: str
    mode: str = "fast"
    model: str = "gpt-4o-mini"

