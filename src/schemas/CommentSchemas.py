from pydantic import BaseModel, Field 
from uuid import uuid4

class CreateCommentSchema(BaseModel):
   body: str = Field(str, min_length=6, max_length=1000)
