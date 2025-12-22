import secrets
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI
from app.schemas.schemas import EmailIn
from app.utils.send_mail import send_code
from app.utils.security import hash_code
from app.service.email_codes import create
from app.data.sqlalchemy_el import Email_code
from app.web.router import main_router
     
app = FastAPI(title="Group-Chat Application")
app.include_router(router=main_router, prefix="/api/v1")

@app.post("/", tags=["root"])
def root(body : EmailIn):
    code = f"{secrets.randbelow(1_000_000):06d}"
    create(Email_code(email=body.email, hashed_code=hash_code(code), verified=False, created_at=datetime.now(timezone.utc)))
    return send_code(body.email, code)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8081, reload=True)
    