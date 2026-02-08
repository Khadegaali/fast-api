from sqlalchemy.orm import Session
from app.users.models.user_model import User
from app.users.schemas.user_schema import UserCreate   # ← هنا التعديل المهم


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, user_data: UserCreate):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    user.name = user_data.name
    user.email = user_data.email
    user.password = user_data.password

    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user_id: int, user_data: dict):
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    for key, value in user_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user