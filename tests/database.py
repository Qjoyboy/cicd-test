from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

DATABASE_URL = (
    "postgresql+asyncpg://"
    "todo_user:password@localhost:5433/todo_test_db"
)

engine_test = create_async_engine(DATABASE_URL, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test,
    class_=AsyncSession,
    expire_on_commit=False
)