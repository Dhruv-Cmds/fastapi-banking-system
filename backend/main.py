from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from contextlib import asynccontextmanager
import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy import text

from backend.db import engine, Base
from backend.routes import auth, account

from backend.core import limiter



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


# App instance
app = FastAPI(lifespan=lifespan)

#  Attach limiter to app
app.state.limiter = limiter


#  Handle rate limit errors
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, slow down"}
    )

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")