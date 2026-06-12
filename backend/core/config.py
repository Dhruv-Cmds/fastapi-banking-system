import os

from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / "docker" / ".env")

ENV = os.getenv("ENV", "dev")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

MAX_DEPOSIT = 50000
MAX_WITHDRAW = 20000
MAX_TRANSFER = 100000


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variable")