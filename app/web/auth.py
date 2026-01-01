import json
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Response
from app.schemas.schemas import VerifyCode, LogIn, TokensOut
from app.service.email_codes import get_one, modify
from app.service.users import create, get_one
from app.service.refresh_tokens import create
from app.schemas.models import Email_code, User, Refresh_token
from app.utils.security import hash_code
from app.utils.auth_config import auth
from app.service import users, refresh_tokens, email_codes


router = APIRouter()

def _store_tokens(email : str, refresh_token : str, revoked : bool):
    creation_time = datetime.now(timezone.utc)
    expiration_time = creation_time + auth.config.JWT_REFRESH_TOKEN_EXPIRES
    return refresh_tokens.create(Refresh_token(email=email, hashed_token=hash_code(refresh_token), expires_at=expiration_time, created_at=creation_time, revoked=revoked))

def _get_pair_tokens(email : str) -> TokensOut:
    access_token = auth.create_access_token(uid=email)
    refresh_token = auth.create_refresh_token(uid=email)

    _store_tokens(email, refresh_token, False) 

    return TokensOut(access_token=access_token, refresh_token=refresh_token)


@router.post("/verify-code")
def code_verification(body : VerifyCode):
    code_h = hash_code(body.code)
    code_from_db = email_codes.get_one(body.email)

    if not code_from_db:
        raise HTTPException(status_code=401, detail="Request code first")
    if code_h != code_from_db.hashed_code.get_secret_value():
        raise HTTPException(status_code=401, detail="Invalid code")
    
    code_from_db.verified = True
    return email_codes.modify(code_from_db)

@router.post("/login")
def create_user(body : LogIn, response : Response):
    users.create(User(email=body.email, username=body.username, created_at=datetime.now(timezone.utc)))
    tokens_pair : TokensOut = _get_pair_tokens(body.email)
    response.set_cookie(key="chat-access-token", value=tokens_pair.access_token)
    return tokens_pair


