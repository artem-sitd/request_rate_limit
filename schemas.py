from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    nickname: str
    phone: str


class UserSchema(BaseModel):
    id: int
    nickname: str
    phone: str

    class Config:
        orm_mode = True


class MessageCreateSchema(BaseModel):
    conversation_id: int
    sender_id: int
    content: str


class MessageSchema(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str

    class Config:
        orm_mode = True
