import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.dialects.postgresql import UUID
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False) 

    user_items = relationship("UserItem", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")