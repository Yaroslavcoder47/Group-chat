from app.data.sqlalchemy_el import Database
from app.schemas.models import Refresh_token

db = Database()

def get_all() -> list[Refresh_token]:
    return db.get_all_refresh_token()

def get_one(user: Refresh_token) -> Refresh_token:
    return db.get_refresh_token()

def create() -> Refresh_token:
    return db.create_refresh_token()

def modify(user: Refresh_token) -> Refresh_token:
    return db.modify_refresh_token()

def delete(user: Refresh_token) -> bool:
    return db.delete_refresh_token()
