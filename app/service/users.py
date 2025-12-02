from app.data.sqlalchemy_el import Database
from app.schemas.models import User

db = Database()

def get_all() -> list[User]:
    return db.get_all_users()

def get_one(user: User) -> User:
    return db.get_user()

def create() -> User:
    return db.create_user()

def modify(user: User) -> User:
    return db.modify_user()

def delete(user: User) -> bool:
    return db.delete_user()
