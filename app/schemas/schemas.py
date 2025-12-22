from pydantic import BaseModel, Field, EmailStr


class EmailIn(BaseModel):
    email : EmailStr

class VerifyCode(BaseModel):
    email : EmailStr
    code: str = Field(..., pattern=r"^\d{6}$")

class LogIn(BaseModel):
    email : EmailStr
    username : str = Field(min_length=3, max_length=15)

class ChatSelection(BaseModel):
    username : str = Field(min_length=3, max_length=15)
    chat : str