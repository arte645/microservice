from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CreateCommentSchema(BaseModel):
   body: str = Field(..., min_length=6, max_length=1000)


class CommentResponseSchema(BaseModel):
   comment_id: UUID
   body: str
   article_id: Optional[UUID]
   user_id: Optional[UUID]
   is_deleted: bool = False

   model_config = ConfigDict(from_attributes=True)
