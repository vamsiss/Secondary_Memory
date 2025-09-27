# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    messages = relationship(
        "ChatMessage", back_populates="chat", cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String)
    content = Column(Text)
    chat = relationship("Chat", back_populates="messages")
