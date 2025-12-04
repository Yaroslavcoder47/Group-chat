from app.data.sqlalchemy_el import Database
from app.schemas.models import User

db = Database()

def get_all() -> list[User]:
    return db.get_all_users()

def get_one(user: User) -> User:
    return db.get_user(user.email)

def create(user: User) -> User:
    return db.create_user(user)

def modify(user: User) -> User:
    return db.modify_user(user.email, user.username)

def delete(user: User) -> bool:
    return db.delete_user(user.email)
