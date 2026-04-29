
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# quote_plus = convert special characters into string.
from urllib.parse import quote_plus
from dotenv import load_dotenv


import os

#  Load environment variables
load_dotenv()


# Read DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")


# Safety checks (VERY IMPORTANT)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("Database environment variables are not properly set")

# Build database URL
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

#  Create engine with production-safe settings
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,     #  Avoid stale connections
    pool_size=10,           #  Connection pool size
    max_overflow=20,        #  Extra connections if needed
    echo=False              #  Disable SQL logs in production
)


# Session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_= AsyncSession,
    expire_on_commit=False,
    autoflush=False
)
