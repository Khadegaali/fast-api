from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.tables.services.embedding_service import EmbeddingService
from app.client.llm_client.cohere_client import CohereClient
from app.tables.schemas.embedding_schema import EmbeddingRequest, EmbeddingResponse
from app.core.deps import get_current_user_id
from uuid import UUID
router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"] 
)
cohere_client = CohereClient()

@router.post("/embed", response_model=EmbeddingResponse)
async def embed_text(
    request: EmbeddingRequest,
    db: Session = Depends(get_db),
    current_user_id: UUID = Depends(get_current_user_id),
):
    embedding = cohere_client.get_embedding(request.text)

    service = EmbeddingService(db)
    service.store_embedding(
        text=request.text,
        embedding=embedding,
        user_id=current_user_id
    )

    return EmbeddingResponse(embedding=embedding)