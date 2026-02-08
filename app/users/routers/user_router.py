from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal
from app.users.schemas.user_schema import UserCreate, UserResponse, UserUpdate
from app.users.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])
user_service = UserService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    updated = user_service.update_user(db, user_id, user_data)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    updated = user_service.patch_user(
        db,
        user_id,
        user_data.model_dump(exclude_unset=True)
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return None