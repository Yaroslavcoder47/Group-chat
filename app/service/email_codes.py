from app.data.sqlalchemy_el import Database
from app.schemas.models import Email_code

db = Database()

def get_all() -> list[Email_code]:
    return db.get_all_email_code()

def get_one(email : str) -> Email_code:
    return db.get_email_code(email)

def create(code: Email_code) -> Email_code:
    return db.create_email_code(code)

def modify(code: Email_code) -> Email_code:
    return db.modify_email_code(code.email, code.hashed_code.get_secret_value(), code.verified)

def delete(code: Email_code) -> bool:
    return db.delete_email_code(code.email)
