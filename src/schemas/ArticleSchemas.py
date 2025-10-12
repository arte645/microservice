from typing import Optional
from pydantic import BaseModel, Field 
from uuid import uuid4

class CreateArticleSchema(BaseModel):
   title: str = Field(str, min_length=6, max_length=120)
   description: str = Field(str, min_length=6, max_length=250)
   body: str = Field(str, min_length=300)
   taglist: Optional[list] = Field(list)
   user_id: str = Field(str)
