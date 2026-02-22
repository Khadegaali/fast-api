from app.tables.repositories.message_repository import MessageRepository, ConversationRepository
from uuid import UUID

class ChatService:
    def __init__(self, db):
        self.db = db
        self.message_repo = MessageRepository(db)
        self.conversation_repo = ConversationRepository(db)

    def build_conversation(self, messages):
    
        conversation = ""
        for msg in messages:
            conversation += f"{msg.role}: {msg.content}\n"
        return conversation

    def process_chat(self, user_id: int, conversation_id: UUID, message: str, cohere_client, max_tokens=500):
   
        conversation = self.conversation_repo.get_by_id(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")


        
        old_messages = self.message_repo.get_conversation_messages(conversation_id)

        
        conversation_text = self.build_conversation(old_messages)
        conversation_text += f"assistant:"

        
        response = cohere_client.generate_text(conversation_text, max_tokens=max_tokens)

    
        self.message_repo.save(conversation_id, "assistant", response)

        self.conversation_repo.update_timestamp(conversation_id)

        return response0