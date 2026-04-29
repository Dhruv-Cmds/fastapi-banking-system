from dotenv import load_dotenv
from pathlib import Path
import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from urllib.parse import quote_plus


# ===== LOAD ENV BASED ON MODE =====
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV = os.getenv("ENV", "dev")

if ENV == "docker":
    env_path = BASE_DIR / "docker" / ".env"
else:
    env_path = BASE_DIR / ".env"

load_dotenv(env_path)


# ===== READ DB CONFIG =====
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD") or "")

# dynamic switching
if ENV == "test":
    DB_NAME = os.getenv("TEST_DB_NAME")
    DB_HOST = "127.0.0.1"
    DB_PORT = "3008"  

elif ENV == "docker":
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DOCKER_DB_HOST") or os.getenv("DB_HOST")
    DB_PORT = "3306"

else:
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "3306")


# ===== SAFETY CHECK =====
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("Database environment variables are not properly set")


# ===== DATABASE URL =====
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# ===== ENGINE =====
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    echo=False
)


# ===== SESSION =====
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)