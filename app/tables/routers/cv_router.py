from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.tables.services.cv_service import CVService
from app.tables.schemas.cv_schema import CVResponse
from app.core.deps import get_current_user_id

router = APIRouter(prefix="/cv", tags=["CV"])

@router.post("/upload", response_model=CVResponse)
async def upload_cv(
    file: UploadFile = File(...),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    service = CVService(db)
    return await service.upload_cv(user_id=current_user_id, file=file)

@router.get("/user/{user_id}", response_model=CVResponse)
async def get_user_cv(
    user_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CVService(db)
    cv = service.repo.get_by_user_id(user_id)
    if not cv:
        raise HTTPException(status_code=404, detail="No CV found for this user")
    # Refresh signed URL
    cv.file_url = service.storage.get_signed_url(cv.file_path)
    return cv

@router.get("/me", response_model=CVResponse)
async def get_my_cv(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CVService(db)
    cv = await service.get_my_cv(user_id=current_user_id)
    if not cv:
        raise HTTPException(status_code=404, detail="No CV found")
    return cv

@router.delete("/me")
async def delete_my_cv(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    service = CVService(db)
    cv = service.repo.get_by_user_id(current_user_id)
    if not cv:
        raise HTTPException(status_code=404, detail="No CV found")
    service.storage.delete_cv(cv.file_path)
    service.repo.delete_cv(cv)
    return {"message": "CV deleted successfully"}


