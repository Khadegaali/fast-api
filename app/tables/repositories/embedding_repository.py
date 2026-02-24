from sqlalchemy.orm import Session
from app.tables.models.embedding_model import TextEmbedding
from uuid import UUID


class EmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_embedding(self, text: str, embedding: list[float], user_id: UUID):
        new_embedding = TextEmbedding(
            user_id=user_id,
            text=text,
            embedding=embedding
        )

        self.db.add(new_embedding)
        self.db.commit()
        self.db.refresh(new_embedding)

        return new_embedding
