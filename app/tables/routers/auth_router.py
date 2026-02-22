from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.tables.services.auth_service import AuthService
from app.tables.repositories.user_repository import UserRepository
from app.tables.services.user_service import UserService
from app.tables.schemas.user_schema import LoginRequest, UserCreate

router = APIRouter(prefix="/auth", tags=["Auth"])

# Services
auth_service = AuthService()
user_repository = UserRepository()
user_service = UserService(user_repository)

# Register endpoint
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

# Login endpoint
@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, data.email, data.password)
