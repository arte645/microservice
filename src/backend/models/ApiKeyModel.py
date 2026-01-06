import uuid
from sqlalchemy import Column, String, Text, ForeignKey, ARRAY, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    api_key_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(Text, unique=True, nullable=False)
    description = Column(Text, nullable=False)

