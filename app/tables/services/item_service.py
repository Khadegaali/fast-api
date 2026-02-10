from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.tables.repositories.item_repository import ItemRepository
from app.tables.models.item_model import Item
from app.tables.schemas.item_schema import ItemCreate

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(self, db: Session, item_data: ItemCreate):
        item = Item(name=item_data.name)
        return self.repository.create_item(item)

    def get_all_items(self, db: Session):
        return self.repository.get_all_items()

    def get_item(self, db: Session, item_id: int):
        item = self.repository.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item

    def delete_item(self, db: Session, item_id: int):
        item = self.repository.delete
