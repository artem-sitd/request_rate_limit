from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    sent_messages = relationship("Message", foreign_keys='Message.sender_id', back_populates="sender")
    conversations_as_user1 = relationship("Conversation", foreign_keys='Conversation.user1_id', back_populates="user1")
    conversations_as_user2 = relationship("Conversation", foreign_keys='Conversation.user2_id', back_populates="user2")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.id"))
    user2_id = Column(Integer, ForeignKey("users.id"))
    user1 = relationship("User", foreign_keys='Conversation.user1_id', back_populates="conversations_as_user1")
    user2 = relationship("User", foreign_keys='Conversation.user2_id,', back_populates="conversations_as_user2")
    messages = relationship("Message", back_populates="conversation")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    sender_id = Column(Integer, ForeignKey("users.id"))
    content = Column(String)
    conversation = relationship("Conversation", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
