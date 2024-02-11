from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str = None
    price: float