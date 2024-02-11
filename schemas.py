from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: str = None
    price: float


class ItemResponse(ItemBase):
    id: int


class ItemsResponse(BaseModel):
    items: list[ItemResponse]
    total_length: int

