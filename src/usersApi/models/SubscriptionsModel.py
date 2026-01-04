import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .BaseModel import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscriber_user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))
    target_user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"))

    subscriber_user = relationship("User", foreign_keys='Subscription.subscriber_user_id')
    target_user = relationship("User", foreign_keys='Subscription.target_user_id')
