import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

if ENVIRONMENT == "supabase":
    env_path = BASE_DIR / ".env.supabase"
else:
    env_path = BASE_DIR / ".env.local"

load_dotenv(env_path, override=True)

print(f" Environment: {ENVIRONMENT}")
print(f"Loading from: {env_path}")
print(f"File exists: {env_path.exists()}")

if env_path.exists():
    with open(env_path, 'r') as f:
        print(f"File content preview:\n{f.read()[:200]}")


class Settings:
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: str = os.getenv("SUPABASE_SERVICE_KEY")
    
    # Buckets 
    SUPABASE_BUCKET: str = os.getenv("SUPABASE_BUCKET", "upload_files")      
    SUPABASE_IMAGES_BUCKET: str = os.getenv("SUPABASE_images", "upload_images")  

    def __init__(self):
        print(f"  Settings loaded:")
        print(f"   DB_USER: {self.DB_USER}")
        print(f"   DB_HOST: {self.DB_HOST}")
        print(f"   DB_PORT: {self.DB_PORT}")
        print(f"   BUCKET: {self.SUPABASE_BUCKET}")
        print(f"   IMAGES BUCKET: {self.SUPABASE_IMAGES_BUCKET}")


settings = Settings()
