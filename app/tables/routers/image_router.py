# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from cohere import ClientV2
# from app.client.llm_client.storage_client import ImageStorageClient

# from app.core.config import settings
# from uuid import uuid4
# import base64

# router = APIRouter()

# # Cohere
# co = ClientV2(api_key=settings.COHERE_API_KEY if hasattr(settings, 'COHERE_API_KEY') else __import__('os').getenv("COHERE_API_KEY"))

# # Image Storage Client
# image_storage = ImageStorageClient()  # ← bucket: upload_images


# @router.post("/analyze")
# async def analyze_image(file: UploadFile = File(...)):
#     try:
#         # قراءة الصورة
#         image_bytes = await file.read()

#         # رفع على Supabase - upload_images bucket
#         file_name = f"{uuid4()}_{file.filename}"
        
#         upload_result = image_storage.upload_image(
#             file_path=file_name,
#             file_content=image_bytes,
#             content_type=file.content_type
#         )
        
#         public_url = upload_result["url"]

#         # تحويل لـ base64 للتحليل
#         base64_image = (
#             f"data:{file.content_type};base64,"
#             + base64.b64encode(image_bytes).decode()
#         )

#         # تحليل الصورة بـ Cohere
#         response = co.chat(
#             model="command-a-vision-07-2025",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": "Please describe this image in detail."
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": base64_image,
#                                 "detail": "high"
#                             }
#                         },
#                     ],
#                 }
#             ],
#         )

#         analysis_text = response.message.content[0].text

#         return {
#             "success": True,
#             "filename": file.filename,
#             "file_url": public_url,  # ← من upload_images bucket
#             "analysis": analysis_text
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import APIRouter, UploadFile, File, HTTPException
# from cohere import ClientV2
# from app.client.llm_client.storage_client import ImageStorageClient
# from app.core.config import settings
# import base64

# router = APIRouter()

# co = ClientV2(
#     api_key=settings.COHERE_API_KEY 
#     if hasattr(settings, 'COHERE_API_KEY') 
#     else __import__('os').getenv("COHERE_API_KEY")
# )

# image_storage = ImageStorageClient()


# @router.post("/analyze")
# async def analyze_image(
#     user_id: str,
#     conversation_id: str,
#     file: UploadFile = File(...)
# ):
#     try:
#         # قراءة الصورة
#         image_bytes = await file.read()

#         # 👇 رفع بالصورة داخل user_id/conversation_id
#         upload_result = image_storage.upload_image(
#             user_id=user_id,
#             conversation_id=conversation_id,
#             file_content=image_bytes,
#             content_type=file.content_type
#         )

#         public_url = upload_result["url"]

#         # تحويل لـ base64 للتحليل
#         base64_image = (
#             f"data:{file.content_type};base64,"
#             + base64.b64encode(image_bytes).decode()
#         )

#         response = co.chat(
#             model="command-a-vision-07-2025",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": [
#                         {
#                             "type": "text",
#                             "text": "Please describe this image in detail."
#                         },
#                         {
#                             "type": "image_url",
#                             "image_url": {
#                                 "url": base64_image,
#                                 "detail": "high"
#                             }
#                         },
#                     ],
#                 }
#             ],
#         )

#         analysis_text = response.message.content[0].text

#         return {
#             "success": True,
#             "file_url": public_url,
#             "analysis": analysis_text
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from cohere import ClientV2
# from app.client.llm_client.storage_client import ImageStorageClient
# from app.core.config import settings
# import base64
# from uuid import uuid4
# router = APIRouter()

#  co = ClientV2(
#     api_key=settings.COHERE_API_KEY 
#     if hasattr(settings, 'COHERE_API_KEY') 
#     else __import__('os').getenv("COHERE_API_KEY")
#  )
# image_storage = ImageStorageClient()
# @router.post("/analyze")
# async def analyze_image(
#     user_id: str,
#     file: UploadFile = File(...),
#     conversation_id: str = None  # ممكن يبقى null
# ):
#     try:
#         image_bytes = await file.read()
#         filename = f"{uuid4()}_{file.filename}"

#         upload_result = image_storage.upload_image(
#             user_id=user_id,
#             file_content=image_bytes,
#             filename=filename,
#             conversation_id=conversation_id
#         )

#         public_url = upload_result["url"]
#         conversation_id_used = upload_result["conversation_id"]

#         # تحويل للصورة لـ base64 للتحليل
#         base64_image = f"data:{file.content_type};base64," + base64.b64encode(image_bytes).decode()

#         response = co.chat(
#             model="command-a-vision-07-2025",
#             messages=[{
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": "Please describe this image in detail."},
#                     {"type": "image_url", "image_url": {"url": base64_image, "detail": "high"}}
#                 ]
#             }]
#         )
#         analysis_text = response.message.content[0].text

#         return {
#             "success": True,
#             "file_url": public_url,
#             "conversation_id": conversation_id_used,
#             "analysis": analysis_text
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")

# from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
# from cohere import ClientV2
# from app.client.llm_client.storage_client import ImageStorageClient
# from app.core.config import settings
# import base64
# from uuid import uuid4

# router = APIRouter()

# co = ClientV2(
#     api_key=settings.COHERE_API_KEY 
#     if hasattr(settings, 'COHERE_API_KEY') 
#     else __import__('os').getenv("COHERE_API_KEY")
# )

# image_storage = ImageStorageClient()

# @router.post("/analyze")
# async def analyze_image(
#     file: UploadFile = File(...),
#     conversation_id: str = None,  # لو موجود يبقى نستخدمه، لو لا نعمل UUID جديد
#     prompt: str = None            # نص اختياري للتحليل
# ):
#     try:
#         # قراءة الصورة
#         image_bytes = await file.read()
#         filename = f"{uuid4()}_{file.filename}"

#         # رفع الصورة على Supabase داخل folder conversation_id
#         upload_result = image_storage.upload_image(
#             file_content=image_bytes,
#             filename=filename,
#             conversation_id=conversation_id
#         )

#         public_url = upload_result["url"]
#         conversation_id_used = upload_result["conversation_id"]

#         # تحويل الصورة إلى Base64 للتحليل
#         base64_image = f"data:{file.content_type};base64," + base64.b64encode(image_bytes).decode()

#         # تحليل الصورة باستخدام Cohere Vision AI
#         response = co.chat(
#             model="command-a-vision-07-2025",
#             messages=[{
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt or "Please describe this image in detail."},
#                     {"type": "image_url", "image_url": {"url": base64_image, "detail": "high"}}
#                 ]
#             }]
#         )
#         analysis_text = response.message.content[0].text

#         return {
#             "success": True,
#             "file_url": public_url,
#             "conversation_id": conversation_id_used,
#             "analysis": analysis_text
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Image analysis failed: {str(e)}")








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
    """
    Analyze image with Cohere Vision AI
    ⚠️ Requires JWT authentication
    """
    try:
        conv_repo = ConversationRepository(db)
        msg_repo = MessageRepository(db)
        
        # Convert conversation_id to UUID if provided
        conv_uuid = None
        is_new_conversation = False
        
        if conversation_id:
            try:
                conv_uuid = UUID(conversation_id)
                # تأكد إن الـ conversation موجودة
                conversation = conv_repo.get_by_id(conv_uuid, current_user_id)
                if not conversation:
                    raise HTTPException(status_code=404, detail="Conversation not found")
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid conversation_id format")
        
        # لو مفيش conversation_id، اعمل واحدة جديدة
        if not conv_uuid:
            conversation = conv_repo.create(
                user_id=current_user_id,
                title="Image Analysis"
            )
            conv_uuid = conversation.id
            is_new_conversation = True
        
        # قراءة الصورة
        image_bytes = await file.read()
        filename = f"{uuid4()}_{file.filename}"

        # رفع الصورة على Supabase Storage
        upload_result = image_storage.upload_image(
            user_id=str(current_user_id),
            file_content=image_bytes,
            filename=filename,
            conversation_id=str(conv_uuid),
            content_type=file.content_type or "image/jpeg"
        )

        public_url = upload_result["file_url"]
        file_path = upload_result["file_path"]

        # تحويل الصورة إلى Base64
        base64_image = f"data:{file.content_type};base64," + base64.b64encode(image_bytes).decode()

        # تحليل الصورة
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
        
        # حفظ رسالة الـ user (الصورة)
        msg_repo.save(
            conversation_id=conv_uuid,
            role="user",
            content=prompt or "Image uploaded",
            file_path=file_path,
            file_url=public_url,
            file_name=filename
        )
        
        # حفظ رد الـ AI
        msg_repo.save(
            conversation_id=conv_uuid,
            role="assistant",
            content=analysis_text
        )
        
        # لو conversation جديدة، حدّث الـ title
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