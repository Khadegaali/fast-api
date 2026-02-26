from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.tables.services.video_service import VideoService
from app.tables.schemas.video_schema import VideoUploadResponse, VideoResponse, ChunkResponse
from app.core.deps import get_current_user_id

router = APIRouter(prefix="/videos", tags=["Smart Video Search"])

@router.post("/upload", response_model=VideoResponse)
async def upload_video(
    file: Optional[UploadFile] = File(None),
    video_url: Optional[str] = Form(None),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if not file and not video_url:
        raise HTTPException(status_code=400, detail="You must provide either a file or a video_url")
    if file and video_url:
        raise HTTPException(status_code=400, detail="Please choose only one option: file or video_url.")

    service = VideoService(db)

    if file:
        return await service.upload_video_file(user_id=current_user_id, file=file)
    else:
        return await service.upload_video_url(user_id=current_user_id, video_url=video_url)


@router.get("/my-videos", response_model=List[VideoResponse])
async def get_my_videos(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = VideoService(db)
    return service.repo.get_user_videos(current_user_id)


@router.get("/user/{user_id}/videos", response_model=List[VideoResponse])
async def get_user_videos(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = VideoService(db)
    return service.repo.get_user_videos(user_id)


@router.get("/chunks/{chunk_id}", response_model=ChunkResponse)
async def get_chunk(
    chunk_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = VideoService(db)
    chunk = service.repo.get_chunk_by_id(chunk_id)
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return chunk

@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(
    video_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = VideoService(db)
    video = service.repo.get_video_by_id(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.delete("/{video_id}")
async def delete_video(
    video_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = VideoService(db)
    deleted = service.repo.delete_user_video(video_id, current_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video not found or not yours")
    return {"message": "Video deleted successfully"}
