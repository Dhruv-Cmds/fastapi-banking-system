from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / "docker" / ".env"
load_dotenv(env_path)

from backend.main import app
from backend.dependencies import get_db

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.db.base import Base

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

engine = create_async_engine("sqlite+aiosqlite:///./test.db")

TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.state.limiter.enabled = False

app.dependency_overrides[get_db] = override_get_db

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac