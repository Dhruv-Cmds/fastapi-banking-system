import os
import asyncio
from pathlib import Path
import platform
import sys
from urllib.parse import quote_plus

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


TESTS_DIR = Path(__file__).resolve().parent
BACKEND_DIR = TESTS_DIR.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

sys.path.insert(0, str(BACKEND_DIR))


# ===== LOAD ENV =====
env_path = PROJECT_ROOT / ".env"

os.environ.setdefault("ENV", "test")

if os.getenv("GITHUB_ACTIONS") != "true":
    load_dotenv(env_path)


from app.db import Base
from app.api import get_db
from app.main import app


# ⚠️ keep this for Windows stability
if platform.system() == "Windows":

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )


# ===== DB CONFIG =====
DB_USER = os.getenv("DB_USER")

DB_PASSWORD = quote_plus(
    os.getenv("DB_PASSWORD") or ""
)

ENV = os.getenv("ENV")

if ENV == "docker":

    DB_HOST = "shared-mysql"
    DB_PORT = "3306"

else:

    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3008")

DB_NAME = os.getenv("TEST_DB_NAME")

DATABASE_URL = (
    "mysql+aiomysql://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


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
