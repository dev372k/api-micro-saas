from pydantic import BaseModel, Field
from commons.enums import ModuleType

class Module(BaseModel):
    name: ModuleType 
    key: str
    user_id: str

    