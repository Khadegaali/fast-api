from sqlalchemy.orm import Session
from app.tables.models.user_item_model import UserItem

class UserItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_item(self, user_item: UserItem):
        self.db.add(user_item)
        self.db.commit()
        self.db.refresh(user_item)
        return user_item

    def get_by_user(self, user_id: int):
        return self.db.query(UserItem).filter(UserItem.user_id == user_id).all()

    def get_by_item(self, item_id: int):
        return self.db.query(UserItem).filter(UserItem.item_id == item_id).all()

    def get_user_item(self, user_item_id: int):
        return self.db.query(UserItem).filter(UserItem.id == user_item_id).first()

    def delete_user_item(self, user_item_id: int):
        item = self.get_user_item(user_item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
        return item
