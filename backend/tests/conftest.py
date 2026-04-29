from dotenv import load_dotenv
from pathlib import Path
import os
import asyncio
from urllib.parse import quote_plus

# ===== LOAD ENV =====
env_path = Path(__file__).resolve().parent.parent.parent / "docker" / ".env"
load_dotenv(env_path)

os.environ["ENV"] = "test"

# ⚠️ keep this for Windows stability
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.db.base import Base

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from backend.main import app
from backend.dependencies import get_db




# ===== DB CONFIG =====
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD") or "")
DB_HOST = "127.0.0.1"
DB_PORT = "3008"
DB_NAME = os.getenv("TEST_DB_NAME")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ===== ENGINE PER TEST (CRITICAL FIX) =====
@pytest_asyncio.fixture
async def db_engine():
    engine = create_async_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


# ===== SESSION =====
@pytest_asyncio.fixture
async def db_session(db_engine):
    async_session = sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session


# ===== OVERRIDE DEPENDENCY =====
@pytest_asyncio.fixture(autouse=True)
async def override_db(db_session):
    async def _get_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


# ===== TEST CLIENT =====
@pytest_asyncio.fixture
async def client():
    app.state.limiter.enabled = False

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac