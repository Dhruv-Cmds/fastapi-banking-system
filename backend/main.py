from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from contextlib import asynccontextmanager

import asyncio

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import text

from backend.db import engine, Base
from backend.routes import auth, account, admin, health
from backend.core import limiter, BankingAPIException
from backend.models import User

from backend.services import admin_service


@asynccontextmanager
async def lifespan(app: FastAPI):

    for attempt in range(15):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            async with AsyncSession(engine) as session:
                await admin_service.create_admin(session)

            break

        except OperationalError:
            print(f"Waiting for DB... ({attempt + 1}/15)")
            await asyncio.sleep(2)

    else:
        raise RuntimeError("Database not available")

    yield


app = FastAPI(
    title="FastAPI Banking System",
    description=(
        "Secure banking API for user signup/login, account management, "
        "deposits, withdrawals, transfers, and transaction history. "
        "Use the /api/login endpoint to obtain a JWT access token and "
        "authorize protected endpoints with the Bearer token."
    ),
    version="1.0.0",

    # docs_url=None,
    # redoc_url=None,
    # openapi_url=None,

    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Authentication", 
            "description": "Signup, login, and profile management."
        },
        {
            "name": "Accounts", 
            "description": "Create accounts, deposit, withdraw, transfer, and view transactions."
        },
        {
            "name": "Admin", 
            "description": "Administrative endpoints for admin users."
        },
        {
            "name": "Health", 
            "description": "Service health checks and diagnostics."
        }
    ]
)

app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(BankingAPIException)
async def banking_exception_handler(request: Request, exc: BankingAPIException):
    """Handle all custom banking API exceptions with unified format"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Handle rate limit errors with unified format"""
    return JSONResponse(
        status_code=429,
        content={
            "error": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests. Please slow down."
        }
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bank.dhruvcore.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin.router, prefix="/api", tags=["Admin"])
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(account.router, prefix="/api", tags=["Accounts"])
app.include_router(health.router, tags=["Health"])
