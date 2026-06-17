from unittest.mock import AsyncMock, MagicMock

from httpx import AsyncClient, ASGITransport
from sqlalchemy import text
from internal.celery.tasks import send_task_created_notification
from main import app
from tests.database import TestingSessionLocal, engine_test
from internal.db.base import Base
from internal.redis.redis import redis_client
from internal.db.session import get_db
from internal.models import *
import pytest_asyncio
from internal.celery.celery_app import celery_app

celery_app.conf.task_always_eager = True

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db
from internal.db.base import Base
from tests.database import engine_test

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    
@pytest_asyncio.fixture(autouse=True)
async def clean_db():

    async with TestingSessionLocal() as session:

        await session.execute(
            text(
                "TRUNCATE TABLE tasks, users RESTART IDENTITY CASCADE"
            )
        )

        await session.commit()

    yield
    
@pytest_asyncio.fixture(autouse=True)
async def mock_external_services():
    redis_client.flushdb = AsyncMock()
    redis_client.get = AsyncMock(return_value=None)
    redis_client.set = AsyncMock()

    send_task_created_notification.delay = MagicMock()

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac