from supabase import create_client, Client
from app.core.config import settings
from uuid import uuid4
from datetime import datetime

class StorageClient:
   

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET  

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
        content_type: str = "image/jpeg",  
        role: str = "user",
        content: str = ""
    ):
        try:
           
            if not conversation_id:
                conversation_id = str(uuid4())

            
            file_path = f"{user_id}/{conversation_id}/{filename}"

        
            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}  
            )

            file_url = self.client.storage.from_(self.bucket).get_public_url(file_path)

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

class VideoStorageClient:

    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_VIDEOS_BUCKET

    def upload_video(self, user_id: str, file_content: bytes, filename: str):
        
        try:
            from uuid import uuid4
            
            file_extension = filename.split('.')[-1] if '.' in filename else 'mp4'
            unique_filename = f"{uuid4().hex}.{file_extension}"
            file_path = f"{user_id}/{unique_filename}"
            
            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": "video/mp4"}
            )
            
            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
            
            return {
                "path": file_path,
                "url": public_url
            }
        except Exception as e:
            raise Exception(f"Video upload failed: {str(e)}")

class CVStorageClient:
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_CV_BUCKET

    def upload_cv(self, user_id: str, file_content: bytes, filename: str) -> dict:
        try:
            file_path = f"{user_id}/{filename}"
            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": "application/pdf", "upsert": "true"}
            )
            signed = self.client.storage.from_(self.bucket).create_signed_url(file_path, 3600)
            return {
                "file_path": file_path,
                "file_url": signed["signedURL"],
                "file_name": filename
            }
        except Exception as e:
            raise Exception(f"CV upload failed: {str(e)}")

    def delete_cv(self, file_path: str):
        try:
            self.client.storage.from_(self.bucket).remove([file_path])
        except Exception:
            pass

    def get_signed_url(self, file_path: str, expires_in: int = 3600) -> str:
        signed = self.client.storage.from_(self.bucket).create_signed_url(file_path, expires_in)
        return signed["signedURL"]