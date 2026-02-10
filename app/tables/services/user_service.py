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
        if self.user_repository.get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        user_data = user.model_copy()
        user_data.password = hash_password(user.password)
        db_user = self.user_repository.create_user(db, user_data)
        return UserResponse.from_orm(db_user)

    # ================= READ ALL
    def get_users(self, db: Session) -> list[UserResponse]:
        users = self.user_repository.get_all_users(db)
        return [UserResponse.from_orm(u) for u in users]

    # ================= READ ONE
    def get_user(self, db: Session, user_id: int) -> UserResponse:
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)

    # ================= UPDATE FULL
    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> UserResponse:
        update_data = user_data.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["password"] = hash_password(update_data["password"])
        user = self.user_repository.update_user(db, user_id, update_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)

    # ================= PATCH PARTIAL
    def patch_user(self, db: Session, user_id: int, user_data: dict) -> UserResponse:
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])
        user = self.user_repository.patch_user(db, user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponse.from_orm(user)

    # ================= DELETE
    def delete_user(self, db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return {"detail": f"User {user_id} deleted successfully"}
