
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.database import get_db
from app.client.llm_client.cohere_client import CohereClient
from app.tables.services.chat_service import ChatService
from app.tables.repositories.message_repository import ConversationRepository, MessageRepository
from app.core.deps import get_current_user_id
from fastapi import Query
router = APIRouter(prefix="/llm", tags=["LLM"])
cohere_client = CohereClient()

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str
    max_tokens: int = 500

class NewConversationRequest(BaseModel):
    title: Optional[str] = "New Chat"


@router.post("/chat")
def chat(
    message: str,
    conversation_id: Optional[int] = Query(None),
    max_tokens: int = 500,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    chat_service = ChatService(db)
    conv_repo = ConversationRepository(db)

    if not conversation_id:
        conversation = conv_repo.create(
            user_id=current_user_id,
            first_message=message
        )
        conversation_id = conversation.id

    try:
        response = chat_service.process_chat(
            user_id=current_user_id,
            conversation_id=conversation_id,
            message=message,
            cohere_client=cohere_client,
            max_tokens=max_tokens
        )

        return {
            "conversation_id": conversation_id,
            "response": response
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/conversations") 
def get_my_conversations(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = ConversationRepository(db)
    conversations = repo.get_user_conversations(current_user_id)
    msg_repo = MessageRepository(db)
    return {
        "conversations": [
            {
                "id": conv.id,
                "title": conv.title,
                "created_at": conv.created_at,
                "updated_at": conv.updated_at,
                "message_count": len(msg_repo.get_conversation_messages(conv.id))
            }
            for conv in conversations
        ]
    }


@router.get("/conversations/{conversation_id}")
def get_conversation(
    conversation_id: int,
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
        "id": conversation.id,
        "title": conversation.title,
        "created_at": conversation.created_at,
        "messages": [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(
    conversation_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    repo = ConversationRepository(db)
    deleted = repo.delete(conversation_id, current_user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"detail": "Conversation deleted"}

