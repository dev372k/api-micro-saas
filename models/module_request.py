from pydantic import BaseModel, Field

class ModuleRequest(BaseModel):
    name: str=Field()
    key: str