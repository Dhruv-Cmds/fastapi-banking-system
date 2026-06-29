import os

from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

ENV = os.getenv("ENV", "dev")

class Setting:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

setting = Setting()

if not setting.SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variable")


MAX_DEPOSIT = 50000
MAX_WITHDRAW = 20000
MAX_TRANSFER = 100000