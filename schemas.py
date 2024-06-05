# schemas.py
from pydantic import BaseModel

class UserCreate(BaseModel):
    nickname: str
    phone: str

class User(BaseModel):
    id: int
    nickname: str
    phone: str

    class Config:
        orm_mode = True

class MessageCreate(BaseModel):
    conversation_id: int
    sender_id: int
    content: str

class Message(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str

    class Config:
        orm_mode = True
