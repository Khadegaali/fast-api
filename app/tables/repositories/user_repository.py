from sqlalchemy.orm import Session
from app.tables.models.user_model import User
from app.tables.schemas.user_schema import UserCreate
from app.core.security import hash_password

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate):
        db_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password)  # ⚡ تخزين الباسورد مشفر
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def update_user(self, user_id: int, user_data: dict):
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            if key == "password":
                setattr(user, "password", hash_password(value))
            else:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user
