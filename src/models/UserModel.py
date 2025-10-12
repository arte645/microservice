import uuid
from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
    sex = Column(Text)
    image_url = Column(Text)
    is_deleted = Column(Boolean, default=False)

    articles = relationship("Article", back_populates="user", cascade="save-update, merge")
    comments = relationship("Comment", back_populates="user", cascade="save-update, merge")
