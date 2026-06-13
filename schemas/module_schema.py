from pydantic import BaseModel, Field
from bson import ObjectId

class Module(BaseModel):
    name: str
    key: str
    user_id: str

    