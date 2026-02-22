from pydantic import BaseModel

class UserItemBase(BaseModel):
    user_id: int
    item_id: int

class UserItemCreate(UserItemBase):
    pass

class UserItemResponse(UserItemBase):
    id: int

    class Config:
        orm_mode = True
