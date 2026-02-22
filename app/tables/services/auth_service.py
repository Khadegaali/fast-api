from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.tables.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, db: Session, email: str, password: str):
    user = self.user_repository.get_user_by_email(db, email)  # ⚡ لازم تبعتي db
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(password, user.password):  # ⚡ مقارنة بالباسورد المشفر
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

