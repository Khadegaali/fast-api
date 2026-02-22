# from supabase import create_client, Client
# from app.core.config import settings

# class StorageClient:
#     def __init__(self):
#         self.client: Client = create_client(
#             settings.SUPABASE_URL,
#             settings.SUPABASE_KEY
#         )
#         self.bucket = settings.SUPABASE_BUCKET
    
#     def upload_file(self, file_path: str, file_content: bytes, content_type: str = "application/octet-stream"):
        
#         try:
#             # Upload file
#             self.client.storage.from_(self.bucket).upload(
#                 path=file_path,
#                 file=file_content,
#                 file_options={"content-type": content_type}
#             )
            
#             # Get public URL
#             public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
            
#             return {
#                 "path": file_path,
#                 "url": public_url
#             }
#         except Exception as e:
#             raise Exception(f"Upload failed: {str(e)}")

# from supabase import create_client, Client
# from app.core.config import settings


# class StorageClient:
#     """للـ chat files - bucket: upload_files"""
#     def __init__(self):
#         self.client: Client = create_client(
#             settings.SUPABASE_URL,
#             settings.SUPABASE_KEY
#         )
#         self.bucket = settings.SUPABASE_BUCKET  # upload_files

#     def upload_file(self, file_path: str, file_content: bytes, content_type: str = "application/octet-stream"):
#         try:
#             self.client.storage.from_(self.bucket).upload(
#                 path=file_path,
#                 file=file_content,
#                 file_options={"content-type": content_type}
#             )
#             public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
#             return {
#                 "path": file_path,
#                 "url": public_url
#             }
#         except Exception as e:
#             raise Exception(f"Upload failed: {str(e)}")

#     def delete_file(self, file_path: str):
#         try:
#             self.client.storage.from_(self.bucket).remove([file_path])
#             return True
#         except Exception as e:
#             raise Exception(f"Delete failed: {str(e)}")


# class ImageStorageClient:
   
#     def __init__(self):
#         self.client: Client = create_client(
#             settings.SUPABASE_URL,
#             settings.SUPABASE_KEY
#         )
#         self.bucket = settings.SUPABASE_IMAGES_BUCKET  # upload_images

#     def upload_image(self, user_id: str,conversation_id: str, file_content: bytes, content_type: str = "image/jpeg"):
#         try:
#             self.client.storage.from_(self.bucket).upload(
#                 path=file_path,
#                 file=file_content,
#                 file_options={"content-type": content_type}
#             )
#             public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
#             return {
#                 "path": file_path,
#                 "url": public_url
#             }
#         except Exception as e:
#             raise Exception(f"Image upload failed: {str(e)}")

#     def delete_image(self, file_path: str):
#         try:
#             self.client.storage.from_(self.bucket).remove([file_path])
#             return True
#         except Exception as e:
#             raise Exception(f"Delete failed: {str(e)}")








from supabase import create_client, Client
from app.core.config import settings
from uuid import uuid4
from datetime import datetime

class StorageClient:
    """للـ chat files - bucket: upload_files"""

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET  # upload_files

    def upload_file(
        self,
        user_id: str,
        conversation_id: str,
        file_content: bytes,
        content_type: str = "application/octet-stream"
    ):
        try:
            file_uuid = str(uuid4())
            extension = content_type.split("/")[-1]

            file_path = f"{user_id}/{conversation_id}/{file_uuid}.{extension}"

            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={
                    "content-type": content_type,
                    "upsert": False
                }
            )

            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

            return {
                "path": file_path,
                "url": public_url
            }

        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def delete_file(self, file_path: str):
        try:
            self.client.storage.from_(self.bucket).remove([file_path])
            return True
        except Exception as e:
            raise Exception(f"Delete failed: {str(e)}")

class ImageStorageClient:
    """رفع الصور على Storage"""
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_IMAGES_BUCKET

    def upload_image(
        self,
        user_id: str,
        file_content: bytes,
        filename: str,
        conversation_id: str = None,
        content_type: str = "image/jpeg",  # ← أضفنا ده!
        role: str = "user",
        content: str = ""
    ):
        try:
            # لو conversation_id مش موجود → نعمل UUID جديد
            if not conversation_id:
                conversation_id = str(uuid4())

            # path داخل Storage
            file_path = f"{user_id}/{conversation_id}/{filename}"

            # رفع الصورة على Storage
            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}  # ← استخدمناه هنا
            )

            file_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

            # حفظ في messages table
            self.client.table("messages").insert({
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "file_path": file_path,
                "file_url": file_url,
                "file_name": filename,
                "created_at": datetime.utcnow().isoformat()
            }).execute()

            return {
                "file_path": file_path,
                "file_url": file_url,
                "file_name": filename,
                "conversation_id": conversation_id
            }

        except Exception as e:
            raise Exception(f"Image upload failed: {str(e)}")