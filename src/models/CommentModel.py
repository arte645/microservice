import uuid
from sqlalchemy import Column, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import Base

class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    body = Column(Text, nullable=False)
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.article_id", ondelete="CASCADE"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    is_deleted = Column(Boolean, default=False)

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")
    