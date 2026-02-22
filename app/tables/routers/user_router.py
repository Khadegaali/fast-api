from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.tables.schemas.user_schema import UserUpdate, UserResponse, UserCreate
from app.tables.repositories.user_repository import UserRepository
from app.tables.services.user_service import UserService
from app.core.deps import get_current_user_id



router = APIRouter(prefix="/users", tags=["Users"])

user_repository = UserRepository()
user_service = UserService(user_repository)

# GET MY PROFILE (protected)
@router.get("/me", response_model=UserResponse)
def me(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.get_user(db, user_id)

#CRUD (protected)
@router.get("/", response_model=list[UserResponse])
def get_users(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.get_user(db, user_id)

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.create_user(db, user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.update_user(db, user_id, user)

@router.patch("/{user_id}", response_model=UserResponse)
def patch_user(
    user_id: int,
    user_data: dict,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.patch_user(db, user_id, user_data)

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    return user_service.delete_user(db, user_id)
