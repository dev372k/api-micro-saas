from pydantic import BaseModel

class OptimizeRequest(BaseModel):
    text: str
    mode: str = "fast"