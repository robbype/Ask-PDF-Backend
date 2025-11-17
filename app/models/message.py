from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, func, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum


class RoleEnum(str, enum.Enum):
    user = "user"
    assistant = "assistant"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    role = Column(Enum(RoleEnum), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="messages")
