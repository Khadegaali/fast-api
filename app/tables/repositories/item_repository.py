from sqlalchemy.orm import Session
from app.tables.models.item_model import Item
from app.tables.schemas.item_schema import ItemCreate

class ItemRepository:
    def __init__(self, db: Session):
        self.db = db  # خزن الـ session

    def create_item(self, item: ItemCreate):
        db_item = Item(name=item.name)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_all_items(self):
        return self.db.query(Item).all()

    def get_item_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def update_item(self, item_id: int, item_data: ItemCreate):
        item = self.get_item_by_id(item_id)
        if not item:
            return None

        item.name = item_data.name
        self.db.commit()
