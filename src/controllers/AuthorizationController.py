from dotenv import load_dotenv
import os
from authx import AuthXConfig, AuthX

load_dotenv()
config = AuthXConfig()
config.JWT_COOKIE_CSRF_PROTECT=False
config.JWT_SECRET_KEY = os.getenv("JWT_KEY")
config.JWT_TOKEN_LOCATION = ["headers"]
config.JWT_ACCESS_COOKIE_NAME = "access_token"

security = AuthX(config=config)

def create_access_token(id: str):
    return security.create_access_token(id)
