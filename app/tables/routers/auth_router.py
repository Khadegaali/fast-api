from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.tables.repositories.user_repository import UserRepository
from app.tables.schemas.user_schema import UserCreate, LoginRequest, UserResponse
from app.core.security import verify_password, create_access_token
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)

    existing_user = user_repository.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    return user_repository.create_user(user)


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)

    user = user_repository.get_user_by_email(data.email)

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
