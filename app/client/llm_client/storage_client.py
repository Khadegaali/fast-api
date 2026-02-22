from supabase import create_client, Client
from app.core.config import settings

class StorageClient:
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.bucket = settings.SUPABASE_BUCKET
    
    def upload_file(self, file_path: str, file_content: bytes, content_type: str = "application/octet-stream"):
        
        try:
            # Upload file
            self.client.storage.from_(self.bucket).upload(
                path=file_path,
                file=file_content,
                file_options={"content-type": content_type}
            )
            
            # Get public URL
            public_url = self.client.storage.from_(self.bucket).get_public_url(file_path)
            
            return {
                "path": file_path,
                "url": public_url
            }
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")