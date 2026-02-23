from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
import uuid as uuid_module

from app.database import get_db
from app.client.llm_client.cohere_client import CohereClient
from app.client.llm_client.storage_client import StorageClient
from app.tables.services.chat_service import ChatService
from app.tables.repositories.message_repository import ConversationRepository, MessageRepository
from app.core.deps import get_current_user_id

router = APIRouter(prefix="/llm", tags=["LLM"])
cohere_client = CohereClient()
storage_client = StorageClient()

class NewConversationRequest(BaseModel):
    title: Optional[str] = "New Chat"

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResponse(BaseModel):
    embedding: List[float]


@router.post("/conversations")
def create_conversation(
    data: NewConversationRequest,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = ConversationRepository(db)
    conversation = repo.create(current_user_id, data.title)
    return {
        "conversation_id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at
    }


@router.post("/chat")
async def chat(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    max_tokens: int = Form(500),
    file: Optional[UploadFile] = File(None),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)

    conv_uuid = None
    is_new_conversation = False

    if conversation_id:
        try:
            conv_uuid = UUID(conversation_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid conversation_id format")

    if not conv_uuid:
        conversation = conv_repo.create(user_id=current_user_id, title="New Chat")
        conv_uuid = conversation.id
        is_new_conversation = True

    file_path = file_url = file_name = None

    if file:
        try:
            file_content = await file.read()
            file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
            unique_filename = f"{uuid_module.uuid4().hex}.{file_extension}" if file_extension else uuid_module.uuid4().hex
            file_path = f"user_{current_user_id}/{conv_uuid}/{unique_filename}"

            upload_result = storage_client.upload_file(
                file_path=file_path,
                file_content=file_content,
                content_type=file.content_type or "application/octet-stream"
            )

            file_url = upload_result["url"]
            file_name = file.filename
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    msg_repo.save(
        conversation_id=conv_uuid,
        role="user",
        content=message,
        file_path=file_path,
        file_url=file_url,
        file_name=file_name
    )

    response = chat_service.process_chat(
        user_id=current_user_id,
        conversation_id=conv_uuid,
        message=message,
        cohere_client=cohere_client,
        max_tokens=max_tokens
    )

    if is_new_conversation:
        try:
            smart_title = cohere_client.generate_title(message)
            conv_repo.update_title(conv_uuid, smart_title)
        except Exception as e:
            fallback_title = message[:50] if len(message) > 50 else message
            conv_repo.update_title(conv_uuid, fallback_title)

    return {
        "conversation_id": str(conv_uuid),
        "response": response,
        "file_uploaded": file is not None,
        "file_url": file_url
    }


@router.get("/conversations")
def get_my_conversations(
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = ConversationRepository(db)
    conversations = repo.get_user_conversations(current_user_id)
    return {
        "conversations": [
            {
                "id": str(conv.id),
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
                "message_count": len(conv.messages)
            }
            for conv in conversations
        ]
    }


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: UUID,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    conversation = conv_repo.get_by_id(conversation_id, current_user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = msg_repo.get_conversation_messages(conversation_id)
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "file_url": msg.file_url,
                "file_name": msg.file_name,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: UUID,
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = ConversationRepository(db)
    deleted = repo.delete(conversation_id, current_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"detail": "Conversation deleted"}


@router.post("/embed", response_model=EmbeddingResponse)
async def embed_text(request: EmbeddingRequest):
    """
    Generate embedding vector for a given text using Cohere embed-4.
    """
    embedding = cohere_client.get_embedding(request.text)
    return {"embedding": embedding}