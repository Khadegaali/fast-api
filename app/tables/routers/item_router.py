from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.tables.schemas.item_schema import ItemCreate
from app.tables.repositories.item_repository import ItemRepository
from app.tables.services.item_service import ItemService
from app.database import get_db

router = APIRouter(prefix="/items", tags=["Items"])

def get_item_repository(db: Session = Depends(get_db)):
    return ItemRepository(db)

def get_item_service(repo: ItemRepository = Depends(get_item_repository)):
    return ItemService(repo)

# Endpoints
@router.post("/")
def create_item(item: ItemCreate, service: ItemService = Depends(get_item_service), db: Session = Depends(get_db)):
    return service.create_item(db, item)

@router.get("/")
def get_items(service: ItemService = Depends(get_item_service), db: Session = Depends(get_db)):
    return service.get_all_items(db)