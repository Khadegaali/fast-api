from sqlalchemy.orm import Session
from app.tables.models.user_model import User
from app.tables.schemas.user_schema import UserCreate

class UserRepository:

    def create_user(self, db: Session, user: UserCreate):
        db_user = User(
            name=user.name,
            email=user.email,
            password=user.password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_all_users(self, db: Session):
        return db.query(User).all()

    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def update_user(self, db: Session, user_id: int, user_data: dict):
        user = self.get_user_by_id(db, user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    def patch_user(self, db: Session, user_id: int, user_data: dict):
        return self.update_user(db, user_id, user_data)
