from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class CVResponse(BaseModel):
    id: UUID
    user_id: UUID
    file_name: str
    file_url: str
    file_path: str
    name: Optional[str]
    phone: Optional[str]
    graduation_year: Optional[str]
    education: Optional[str]
    technical_skills: Optional[List[str]] = [] 
    experience: Optional[str]
    summary: Optional[str]

    class Config:
        from_attributes = True