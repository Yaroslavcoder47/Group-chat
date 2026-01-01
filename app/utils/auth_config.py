from authx import AuthX, AuthXConfig
from datetime import timedelta


config = AuthXConfig(
    JWT_SECRET_KEY = "some-secret-key",
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=14),
    JWT_ACCESS_COOKIE_NAME="group-chat-token",
    JWT_COOKIE_CSRF_PROTECT=False,
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_COOKIE_SECURE=True,
)

auth = AuthX(config=config)
