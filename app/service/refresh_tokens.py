from app.data.sqlalchemy_el import Database
from app.schemas.models import Refresh_token

db = Database()

def get_all() -> list[Refresh_token]:
    return db.get_all_refresh_token()

def get_one(token: Refresh_token) -> Refresh_token:
    return db.get_refresh_token(token.email)

def create(token: Refresh_token) -> Refresh_token:
    return db.create_refresh_token(token)

def modify(token: Refresh_token) -> Refresh_token:
    return db.modify_refresh_token(token.email, token.revoked)

def delete(token: Refresh_token) -> bool:
    return db.delete_refresh_token(token.email)
