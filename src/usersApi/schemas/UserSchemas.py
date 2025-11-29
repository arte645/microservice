from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from pydantic import ConfigDict


class CreateUserSchema(BaseModel):
   email: EmailStr = Field(..., min_length=6, max_length=50)
   username: str = Field(..., min_length=6, max_length=25)
   password: str = Field(..., min_length=6, max_length=25)
   sex: Optional[str] = Field(None, max_length=120)
   image_url: Optional[HttpUrl] = None


class LoginUserSchema(BaseModel):
   username: str = Field(..., min_length=6, max_length=25)
   password: str = Field(..., min_length=6, max_length=25)


class UserResponseSchema(BaseModel):
   user_id: UUID
   email: EmailStr
   username: str
   password: str
   sex: Optional[str] = None
   image_url: Optional[HttpUrl] = None
   is_deleted: bool = False

   model_config = ConfigDict(from_attributes=True)
