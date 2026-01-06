from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CreateArticleSchema(BaseModel):
   title: str = Field(..., min_length=6, max_length=120)
   description: str = Field(..., min_length=6, max_length=250)
   body: str = Field(..., min_length=300)
   taglist: List[str] = Field(default_factory=list)


class ArticleResponseSchema(BaseModel):
   article_id: UUID
   title: str
   description: str
   body: str
   taglist: List[str] = Field(default_factory=list)
   user_id: Optional[UUID]
   is_deleted: bool = False
   status: str

   model_config = ConfigDict(from_attributes=True)
