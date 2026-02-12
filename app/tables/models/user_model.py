from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # اسم العمود password بس سيبها hashed في الrepository

    user_items = relationship("UserItem", back_populates="user")
