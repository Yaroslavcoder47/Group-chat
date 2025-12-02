from pydantic import BaseModel, EmailStr, Field, SecretStr
from datetime import datetime

class User(BaseModel):
    email: EmailStr = Field(max_length=40)
    username: str = Field(default="Undefined", max_length=15)
    created_at: datetime 

class Email_code(BaseModel):
    email: EmailStr = Field(max_length=40)
    hashed_code: SecretStr
    verified: bool
    created_at: datetime

class Refresh_token(BaseModel):
    email: EmailStr = Field(max_length=40)
    hashed_token: SecretStr
    expires_at: datetime
    created_at: datetime
    revoked: bool

    