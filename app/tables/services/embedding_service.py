from sqlalchemy.orm import Session
from app.tables.repositories.embedding_repository import EmbeddingRepository
from uuid import UUID
class EmbeddingService:
    def __init__(self, db: Session):
        self.repo = EmbeddingRepository(db)

    def store_embedding(self, text: str, embedding: list[float], user_id: UUID):
        return self.repo.save_embedding(text, embedding, user_id)
