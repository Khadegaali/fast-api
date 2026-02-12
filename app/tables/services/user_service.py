from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.tables.repositories.user_repository import UserRepository
from app.tables.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password
from app.tables.models.user_model import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    # ================= CREATE
    def create_user(self, db: Session, user: UserCreate) -> UserResponse:
        existing_user = self.user_repository.get_user_by_email(user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = self.user_repository.create_user(user)
        return UserResponse.model_validate(db_user)

    # ================= READ ALL
    def get_users(self, db: Session) -> list[UserResponse]:
        users = self.user_repository.get_all_users()
        return [UserResponse.model_validate(u) for u in users]

    # ================= READ ONE
    def get_user(self, db: Session, user_id: int) -> UserResponse:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    # ================= UPDATE FULL
    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> UserResponse:
        update_data = user_data.model_dump(exclude_unset=True)
        user = self.user_repository.update_user(user_id, update_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    # ================= PATCH PARTIAL
    def patch_user(self, db: Session, user_id: int, user_data: dict) -> UserResponse:
        user = self.user_repository.update_user(user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.model_validate(user)

    # ================= DELETE
    def delete_user(self, db: Session, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.db.delete(user)
        self.db.commit()
        return {"detail": f"User {user_id} deleted successfully"}