import secrets
import uvicorn
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.schemas.schemas import EmailIn
from app.utils.send_mail import send_code
from app.utils.security import hash_code
from app.service.email_codes import create
from app.data.sqlalchemy_el import Email_code
from app.web.router import main_router
     
app = FastAPI(title="Group-Chat Application")
app.include_router(router=main_router, prefix="/api/v1")


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse("app/static/index.html")


@app.post("/", tags=["root"])
def root(body : EmailIn):
    code = f"{secrets.randbelow(1_000_000):06d}"
    create(Email_code(email=body.email, hashed_code=hash_code(code), verified=False, created_at=datetime.now(timezone.utc)))
    send_code(body.email, code)
    return JSONResponse(content="Verification code was sent on email")


@app.post("/api/v1/", tags=["root"])
def api_root(body: EmailIn):
    """Compatibility route so frontend posting to /api/v1/ works."""
    return root(body)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8081, reload=True)
    