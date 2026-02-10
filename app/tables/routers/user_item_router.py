from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.tables.schemas.user_item_schema import UserItemCreate
from app.tables.repositories.user_item_repository import UserItemRepository
from app.tables.services.user_item_service import UserItemService

router = APIRouter(prefix="/user-items", tags=["User Items"])

@router.post("/")
def create_user_item(
    user_item: UserItemCreate,
    db: Session = Depends(get_db)
):
    repository = UserItemRepository(db)
    service = UserItemService(repository)
    return service.create_user_item(user_item)
