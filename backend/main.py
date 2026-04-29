from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from backend.db import engine, Base
from backend.routes import auth, account


@asynccontextmanager
async def lifespan(app: FastAPI):

    for attempt in range(15):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break

        except OperationalError:
            print(f"Waiting for DB... ({attempt + 1}/15)")
            await asyncio.sleep(2)

    else:
        raise RuntimeError("Database not available")

    yield


# 🔹 App instance
app = FastAPI(lifespan=lifespan)


# 🔹 Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 🔹 Routes
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")