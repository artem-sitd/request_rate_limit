from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

# from models import User, Conversation, Message
from schemas import UserCreateSchema, UserSchema, MessageCreateSchema, MessageSchema
from database import Base, engine, get_session

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


# создает все таблицы перед стартом fastapi
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/api/users/", response_model=UserSchema)
async def create_user(user: UserCreateSchema,
                      session: AsyncSession = Depends(get_session)):
    async with session.begin():
        db_user = await session.execute(select(users).where(users.c.phone == user.phone))
        db_user = db_user.scalars().first()
        if db_user:
            raise HTTPException(status_code=400, detail="Phone already registered")
        db_user = await session.execute(select(users).where(users.c.nickname == user.nickname))
        db_user = db_user.scalars().first()
        if db_user:
            raise HTTPException(status_code=400, detail="Nickname already registered")
        new_user = users.insert().values(nickname=user.nickname, phone=user.phone)
        await session.execute(new_user)
        await session.commit()
        return user


@app.get("/api/users/", response_model=UserSchema)
async def get_user(query: str,
                   session: AsyncSession = Depends(get_session)):
    async with session.begin():
        db_user = await session.execute(select(users).where(
            or_(users.c.phone == query, users.c.nickname == query)
        ))
        db_user = db_user.scalars().first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.post("/api/conversations/")
async def create_conversation(user1_id: int, user2_id: int,
                              session: AsyncSession = Depends(get_session)):
    async with session.begin():
        new_conversation = conversations.insert().values(user1_id=user1_id, user2_id=user2_id)
        await session.execute(new_conversation)
        await session.commit()
        return {"status": "conversation created"}


@app.post("/api/messages/", response_model=MessageSchema)
async def create_message(message: MessageCreateSchema,
                         session: AsyncSession = Depends(get_session)):
    async with session.begin():
        new_message = messages.insert().values(
            conversation_id=message.conversation_id,
            sender_id=message.sender_id,
            content=message.content
        )
        await session.execute(new_message)
        await session.commit()
        return message


@app.get("/api/messages/{conversation_id}/", response_model=list[MessageSchema])
async def get_messages(conversation_id: int,
                       session: AsyncSession = Depends(get_session)):
    async with session.begin():
        result = await session.execute(select(messages).where(messages.c.conversation_id == conversation_id))
        messages_list = result.scalars().all()
        return messages_list
