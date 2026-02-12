# from app.tables.models.user_model import Base as UserBase
# from app.tables.models.item_model import Base as ItemBase
# from app.tables.models.user_item_model import Base as UserItemBase
# from app.database import engine_local, engine_supabase

# def create_all_tables():
#     # Create tables in local Postgres
#     UserBase.metadata.create_all(bind=engine_local)
#     ItemBase.metadata.create_all(bind=engine_local)
#     UserItemBase.metadata.create_all(bind=engine_local)

#     # Create tables in Supabase
#     UserBase.metadata.create_all(bind=engine_supabase)
#     ItemBase.metadata.create_all(bind=engine_supabase)
#     UserItemBase.metadata.create_all(bind=engine_supabase)

# if __name__ == "__main__":
#     create_all_tables()
#     print("Tables created in both local Postgres and Supabase!")
