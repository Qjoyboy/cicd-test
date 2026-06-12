from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from config import config

# DATABASE_URL = "postgresql+asyncpg://todo_user:password@todo_db:5432/todo_db"

engine = create_async_engine(config.settings.DATABASE_URL)
async_session = async_sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session