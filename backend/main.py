from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from contextlib import asynccontextmanager
from passlib.context import CryptContext

import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text, select

from backend.db import engine, Base
from backend.routes import auth, account, admin
from backend.core import limiter
from backend.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):

    for attempt in range(15):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                
                # create default admin on first run
                async with AsyncSession(engine) as session:
                    result = await session.execute(select(User).where(User.username == "admin"))
                    
                    if not result.scalar_one_or_none():
                        session.add(User(
                            username="admin",
                            name="Admin",
                            password=pwd_context.hash("admin123"),
                            role="admin"
                        ))
                        await session.commit()
                        print("✅ Admin user created: admin / admin123")

            break

        except OperationalError:
            print(f"Waiting for DB... ({attempt + 1}/15)")
            await asyncio.sleep(2)

    else:
        raise RuntimeError("Database not available")

    yield


app = FastAPI(lifespan=lifespan)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests, slow down"}
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(account.router, prefix="/api")