from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID, uuid4
from cohere import ClientV2
from app.client.llm_client.storage_client import ImageStorageClient
from app.tables.repositories.message_repository import MessageRepository, ConversationRepository
from app.core.deps import get_current_user_id
from app.database import get_db
from app.core.config import settings
import base64

router = APIRouter(prefix="/images", tags=["Images"])

co = ClientV2(api_key=settings.COHERE_API_KEY if hasattr(settings, 'COHERE_API_KEY') else __import__('os').getenv("COHERE_API_KEY"))
image_storage = ImageStorageClient()


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    conversation_id: Optional[str] = Form(None),
    prompt: Optional[str] = Form(None),
    current_user_id: UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
  
    try:
        conv_repo = ConversationRepository(db)
        msg_repo = MessageRepository(db)
        
        # Convert conversation_id to UUID if provided
        conv_uuid = None
        is_new_conversation = False
        
        if conversation_id:
            try:
                conv_uuid = UUID(conversation_id)
                conversation = conv_repo.get_by_id(conv_uuid, current_user_id)
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid conversation_id format")
        
       
        if not conv_uuid:
            conversation = conv_repo.create(
                user_id=current_user_id,
                title="Image Analysis"
            )
            conv_uuid = conversation.id
            is_new_conversation = True
        
        
        image_bytes = await file.read()
        filename = f"{uuid4()}_{file.filename}"

        upload_result = image_storage.upload_image(
            user_id=str(current_user_id),
            file_content=image_bytes,
            filename=filename,
            conversation_id=str(conv_uuid),
            content_type=file.content_type or "image/jpeg"
        )

        public_url = upload_result["file_url"]
        file_path = upload_result["file_path"]


        base64_image = f"data:{file.content_type};base64," + base64.b64encode(image_bytes).decode()

        response = co.chat(
            model="command-a-vision-07-2025",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt or "Please describe this image in detail."},
                    {"type": "image_url", "image_url": {"url": base64_image, "detail": "high"}}
                ]
            }]
        )
        
        analysis_text = response.message.content[0].text
        msg_repo.save(
            conversation_id=conv_uuid,
            role="user",
            content=prompt or "Image uploaded",
            file_path=file_path,
            file_url=public_url,
            file_name=filename
        )
        
        msg_repo.save(
            conversation_id=conv_uuid,
            role="assistant",
            content=analysis_text
        )
        
        if is_new_conversation:
            conv_repo.update_title(conv_uuid, "Image Analysis")

        return {
            "success": True,
            "user_id": str(current_user_id),
            "conversation_id": str(conv_uuid),
            "file_url": public_url,
            "analysis": analysis_text
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")
