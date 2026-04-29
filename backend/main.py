from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import engine, Base
import backend.routes.auth as auth_routes
import backend.routes.account as account_routes

from sqlalchemy.exc import OperationalError
from sqlalchemy import text
from contextlib import asynccontextmanager
import asyncio


@asynccontextmanager
async def lifespan(app: FastAPI):

    for i in range(15):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            break

        except OperationalError:
            print(f"⏳ Waiting for DB... {i+1}/15")
            await asyncio.sleep(2)

    else:
        raise RuntimeError("❌ DB never became ready")

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_routes.router, prefix="/api")
app.include_router(account_routes.router, prefix="/api")