from fastapi import FastAPI
from app.database import Base, engine
from app.tables.routers.user_router import router as user_router
from app.tables.routers.item_router import router as item_router
from app.tables.routers.user_item_router import router as user_item_router
from app.tables.routers.auth_router import router as auth_router

# Create tables in the selected database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI project")

app.include_router(user_router)
app.include_router(item_router)
app.include_router(user_item_router)
app.include_router(auth_router)
