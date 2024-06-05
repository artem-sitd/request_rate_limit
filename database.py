# database.py
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = "postgresql+asyncpg://messenger_user:your_password@localhost/messenger_db"

engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()
