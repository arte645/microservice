from dotenv import load_dotenv
import os
from authx import AuthXConfig, AuthX
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security
from fastapi.concurrency import run_in_threadpool

bearer_scheme = HTTPBearer(auto_error=False)

load_dotenv()
config = AuthXConfig()
config.JWT_COOKIE_CSRF_PROTECT = False
config.JWT_SECRET_KEY = os.getenv("JWT_KEY")
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_ACCESS_COOKIE_NAME = "access_token"

security = AuthX(config=config)

def create_access_token(id: str):
    return security.create_access_token(id)

async def access_token_required(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = credentials.credentials
    try:
        # AuthX appears to expose sync decode; run in threadpool to avoid blocking event loop
        user = await run_in_threadpool(security._decode_token, token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
