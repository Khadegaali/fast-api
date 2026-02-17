from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class LLMRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    max_tokens: int = 500


class LLMResponse(BaseModel):
    conversation_id: UUID
    response: str
