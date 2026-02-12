from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.tables.schemas.user_schema import UserUpdate, UserResponse, UserCreate
from app.tables.repositories.user_repository import UserRepository
from app.tables.services.user_service import UserService
from app.core.deps import get_current_user_id
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])

# GET MY PROFILE (protected)
@router.get("/me", response_model=UserResponse)
def me(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service.get_user(db, user_id)

# UPDATE MY PROFILE (protected - own data only)
@router.put("/me", response_model=UserResponse)
def update_me(
    user: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service.update_user(db, current_user_id, user)

@router.patch("/me", response_model=UserResponse)
def patch_me(
    user_data: dict,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service.patch_user(db, current_user_id, user_data)

# DELETE MY ACCOUNT (protected - own data only)
@router.delete("/me")
def delete_me(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service.delete_user(db, current_user_id)

@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user_repo = UserRepository(db)
    service = UserService(user_repo)
    return service.get_users(db)
