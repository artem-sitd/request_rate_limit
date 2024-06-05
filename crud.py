from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_
from models import User, Conversation, Message
from schemas import UserCreateSchema, UserSchema, MessageCreateSchema, MessageSchema
from database import get_session

router = APIRouter()


@router.post("/api/users/", response_model=UserSchema)
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        db_user = await session.execute(
            select(User).where(or_(User.phone == user.phone, User.nickname == user.nickname)))
        db_user = db_user.scalars().first()
        if db_user:
            if db_user.phone == user.phone:
                raise HTTPException(status_code=400, detail="Phone already registered")
            else:
                raise HTTPException(status_code=400, detail="Nickname already registered")
        new_user = User(nickname=user.nickname, phone=user.phone)
        session.add(new_user)
        await session.commit()
        # await session.refresh(new_user)
        return new_user


@router.get("/api/users/", response_model=UserSchema)
async def get_user(query: str, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        db_user = await session.execute(select(User).where(or_(User.phone == query, User.nickname == query)))
        db_user = db_user.scalars().first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@router.post("/api/conversations/")
async def create_conversation(user1_id: int, user2_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        new_conversation = Conversation(user1_id=user1_id, user2_id=user2_id)
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
        return {"status": "conversation created", "conversation": new_conversation.id}


@router.post("/api/messages/", response_model=MessageSchema)
async def create_message(message: MessageCreateSchema, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        new_message = Message(conversation_id=message.conversation_id, sender_id=message.sender_id,
                              content=message.content)
        session.add(new_message)
        await session.commit()
        await session.refresh(new_message)
        return new_message


@router.get("/api/messages/{conversation_id}/", response_model=list[MessageSchema])
async def get_messages(conversation_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(Message).where(Message.conversation_id == conversation_id))
        messages_list = result.scalars().all()
        return messages_list
