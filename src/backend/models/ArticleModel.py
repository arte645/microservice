import uuid
from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import Base


class Article(Base):
    __tablename__ = "articles"

    article_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    taglist = Column(ARRAY(String))
    user_id = Column(UUID(as_uuid=True))
    is_deleted = Column(Boolean, default=False)

    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
