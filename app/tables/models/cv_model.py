from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class CV(Base):
    __tablename__ = "cvs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True)  
    file_path = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    graduation_year = Column(String, nullable=True)
    education = Column(Text, nullable=True)
    technical_skills = Column(Text, nullable=True)
    experience = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default="now()")
    updated_at = Column(TIMESTAMP, server_default="now()", onupdate="now()")