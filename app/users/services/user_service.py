from fastapi import HTTPException
from sqlalchemy.orm import Session

# ──────────────────────────────────────────────────────────────
#  الـ import الصحيح (استبدل الـ import الغلط القديم)
from app.users.repositories.user_repository import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    patch_user,
)

from app.users.schemas.user_schema import UserCreate


class UserService:

    def create_user(self, db: Session, user: UserCreate):
        if get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        return create_user(db, user)

    def get_users(self, db: Session):
        return get_all_users(db)

    def get_user(self, db: Session, user_id: int):
        user = get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, db: Session, user_id: int, user_data: UserCreate):
        user = update_user(db, user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def patch_user(self, db: Session, user_id: int, user_data: dict):
        user = patch_user(db, user_id, user_data)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user