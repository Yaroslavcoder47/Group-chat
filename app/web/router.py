from fastapi import APIRouter
from . import auth, chat

main_router = APIRouter()

main_router.include_router(auth.router, tags=["auth"])
main_router.include_router(chat.router, tags=["chat"])