from typing import Optional
from pydantic import BaseModel, EmailStr, Field 
from uuid import uuid4

class CreateUserSchema(BaseModel):
   email: EmailStr = Field(EmailStr, min_length=6, max_length=50)
   username: str = Field(str, min_length=6, max_length=25)
   password: str = Field(str, min_length=6, max_length=25)
   sex: Optional[str] = Field(None, max_length=120)
   image_url: Optional[str] = Field(None, pattern=r'^https?://', max_length=500)

class LoginUserSchema(BaseModel):
   username: str = Field(str, min_length=6, max_length=25)
   password: str = Field(str, min_length=6, max_length=25)
