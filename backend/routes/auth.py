from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    MessageResponse,
    TokenResponse,
)
from backend.services import user_service
from backend.dependencies import get_current_user
from backend.dependencies.db import get_db
from backend.core.limiter import limiter

router = APIRouter(tags=["Authentication"])


# SIGNUP
@router.post(
    "/signup",
    response_model=MessageResponse,
    summary="Register a new user",
    description="Create a new application user. Passwords are hashed and username must be unique."
)
@limiter.limit("3/second")
async def signup(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.signup_user(db, user)


# LOGIN
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and obtain JWT",
    description=(
        "Authenticate with username and password to receive an access token. "
        "Use the returned Bearer token for protected endpoints via the Authorization header."
    )
)
@limiter.limit("5/minute")
async def login(
    request: Request,
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.login_user(db, user)


# UPDATE PROFILE
@router.put(
    "/me",
    response_model=MessageResponse,
    summary="Update current user profile",
    description="Update name or password for the current user. Requires a valid JWT Bearer token."
)
@limiter.limit("5/second")
async def update_profile(
    request: Request,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await user_service.update_profile(db, data, current_user)