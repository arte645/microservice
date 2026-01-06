from fastapi import Request
from dotenv import load_dotenv
import os
from authx import AuthXConfig, AuthX
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Security
from fastapi.concurrency import run_in_threadpool
from ..repositories.ApiKeysRepository import ApiKeysRepository
from ..specifications.ApiKeySpecifications import ApiKeySpecification
from ..models.Database import AsyncSessionLocal

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
        user = await run_in_threadpool(security._decode_token, token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def inner_token_required(request: Request):
    # Берем заголовок Authorization напрямую
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing authorization")

    # Разделяем по пробелу и берем вторую часть как токен
    try:
        _, api_key = auth_header.strip().split(" ", 1)
    except ValueError:
        raise HTTPException(status_code=403, detail="Invalid authorization header format")

    async with AsyncSessionLocal() as db:
        api_key_row = await ApiKeysRepository(db).filter_by_spec(
            ApiKeySpecification.key_is(api_key.strip())
        )

    if not api_key_row:
        raise HTTPException(status_code=403, detail="Invalid internal token")

    return api_key_row[0]
