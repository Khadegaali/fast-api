from pydantic import BaseModel
from typing import Optional
from uuid import UUID
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        from_attributes = True  

class LoginRequest(BaseModel):
    email: str
    password: str
