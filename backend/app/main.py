from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from contextlib import asynccontextmanager

import asyncio

from sqlalchemy.exc import OperationalError

from sqlalchemy import text

from app.db.models import User, account, transactions
from app.core import BankingAPIException
from app.db import engine, Base
from app.core import limiter

from app.api.routes import accounts_routes, admin_routes, auth_routes, health_routes


@asynccontextmanager
async def lifespan(app: FastAPI):

    for attempt in range(15):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                
            break

        except OperationalError as e:
            print(f"Waiting for DB... ({attempt + 1}/15)")
            await asyncio.sleep(2)
            raise e

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
    # allow_origins=["https://bank.dhruvcore.com/"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(accounts_routes, prefix="/api", tags=["Accounts"])
app.include_router(admin_routes, prefix="/api", tags=["Admin"])
app.include_router(auth_routes, prefix="/api", tags=["Authentication"])
app.include_router(health_routes, tags=["Health"])
