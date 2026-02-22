from fastapi import HTTPException
from app.tables.repositories.user_item_repository import UserItemRepository
from app.tables.schemas.user_item_schema import UserItemCreate
from app.tables.models.user_item_model import UserItem

class UserItemService:
    def __init__(self, repository: UserItemRepository):
        self.repository = repository

    def create_user_item(self, user_item: UserItemCreate):
        db_item = UserItem(
            user_id=user_item.user_id,
            item_id=user_item.item_id
        )
        return self.repository.create_user_item(db_item)

    def get_all_user_items(self):
        return self.repository.get_all_user_items()

    def get_user_item(self, user_item_id: int):
        item = self.repository.get_user_item(user_item_id)
        if not item:
            raise HTTPException(status_code=404, detail="UserItem not found")
        return item

    def delete_user_item(self, user_item_id: int):
        item = self.repository.delete_user_item(user_item_id)
        if not item:
            raise HTTPException(status_code=404, detail="UserItem not found")
        return {"detail": "Deleted successfully"}
