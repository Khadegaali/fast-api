from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

class ChunkResponse(BaseModel):
    chunk_num: int
    total_chunks: int
    content: str

    class Config:
        from_attributes = True

class VideoResponse(BaseModel):
    id: UUID
    youtube_video_id: Optional[str]
    video_url: str
    title: Optional[str]
    description: Optional[str]
    duration: int
    topic: Optional[str]
    chunks: Optional[List[ChunkResponse]] = [] 
    
    
    class Config:
        from_attributes = True

class VideoUploadResponse(VideoResponse):
    pass

class VideoSearchRequest(BaseModel):
    query: str
    limit: int = 10