from pydantic import BaseModel, Field 

class CreateCommentSchema(BaseModel):
   body: str = Field(str, min_length=6, max_length=1000)
