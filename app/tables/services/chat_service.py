from app.tables.repositories.message_repository import MessageRepository, ConversationRepository

class ChatService:
    def __init__(self, db):
        self.db = db
        self.message_repo = MessageRepository(db)
        self.conversation_repo = ConversationRepository(db)

    def build_conversation(self, messages):
        """بناء الـ conversation history للـ AI"""
        conversation = ""
        for msg in messages:
            conversation += f"{msg.role}: {msg.content}\n"
        return conversation

    def process_chat(self, user_id: int, conversation_id: int, message: str, cohere_client, max_tokens=500):
        # 1️⃣ تأكد إن الـ conversation موجودة وبتاعة الـ user
        conversation = self.conversation_repo.get_by_id(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # 2️⃣ احفظ رسالة الـ user
        self.message_repo.save(conversation_id, "user", message)

        # 3️⃣ جيب الـ history
        old_messages = self.message_repo.get_conversation_messages(conversation_id)

        # 4️⃣ ابني الـ conversation text
        conversation_text = self.build_conversation(old_messages)
        conversation_text += f"assistant:"

        # 5️⃣ اتصل بالـ AI
        response = cohere_client.generate_text(conversation_text, max_tokens=max_tokens)

        # 6️⃣ احفظ رد الـ AI
        self.message_repo.save(conversation_id, "assistant", response)

        # 7️⃣ حدّث timestamp
        self.conversation_repo.update_timestamp(conversation_id)

        return response