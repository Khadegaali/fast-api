from pydantic import BaseModel
from datetime import date

class ItemBase(BaseModel):
    name: str


class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
       from_attributes = True
