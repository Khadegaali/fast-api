from sqlalchemy.orm import Session
from uuid import UUID
from app.tables.models.message import Message, Conversation
from datetime import datetime


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: UUID, title: str = None, first_message: str = None):
        if not title and first_message:
            title = first_message[:50] if len(first_message) > 50 else first_message
        elif not title:
            title = "New Chat"

        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_by_id(self, conversation_id: UUID, user_id: UUID):  
        return (
            self.db.query(Conversation)
            .filter(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            .first()
        )

    def get_user_conversations(self, user_id: UUID):  
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    def update_timestamp(self, conversation_id: UUID):
        conversation = (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.db.commit()

    def update_title(self, conversation_id: UUID, new_title: str):
        conversation = (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )
        if not conversation:
            return None

        conversation.title = new_title
        conversation.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def delete(self, conversation_id: UUID, user_id: UUID):  
        conversation = self.get_by_id(conversation_id, user_id)
        if conversation:
            self.db.delete(conversation)
            self.db.commit()
            return True
        return False


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        conversation_id: UUID,
        role: str,
        content: str,
        file_path: str = None,
        file_url: str = None,
        file_name: str = None
    ):
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            file_path=file_path,
            file_url=file_url,
            file_name=file_name
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_conversation_messages(self, conversation_id: UUID):
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )