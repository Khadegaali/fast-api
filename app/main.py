# main.py
from fastapi import FastAPI
from app.database import Base, engine
from app.users.routers.user_router import router as user_router  # <--- هنا

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI CRUD Example")

# إضافة الروترات
app.include_router(user_router)
