import json
from fastapi import APIRouter, HTTPException
from app.schemas.schemas import VerifyCode
from app.service.email_codes import get_one, modify
from app.schemas.models import Email_code
from app.utils.security import hash_code


router = APIRouter()

@router.post("/verify-code")
def code_verification(body : VerifyCode):
    code_h = hash_code(body.code)
    code_from_db = get_one(body.email)

    if not code_from_db:
        raise HTTPException(status_code=401, detail="Request code first")
    if code_h != code_from_db.hashed_code.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid code")
    
    code_from_db.verified = True
    return modify(code_from_db)

