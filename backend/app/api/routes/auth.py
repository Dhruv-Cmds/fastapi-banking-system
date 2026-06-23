from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    TokenResponse,
)
from app.services import user_service
from app.api import get_current_user, get_db
from app.core import limiter
from app.db.models import User
from app.services import auth_service

router = APIRouter(tags=["Authentication"])


# SIGNUP
@router.post(
    "/signup",
    response_model=UserResponse,
    summary="Register a new user",
    description="Create a new application user. Passwords are hashed and username must be unique."
)
@limiter.limit("3/second")
async def signup(
        request: Request,
        user: UserCreate,
        db: AsyncSession = Depends(get_db),
    ):

    return await auth_service.signup(db, user)


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
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await auth_service.login(
        db,
        credentials.username,
        credentials.password
    )


# UPDATE PROFILE
@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user profile",
    description="Update name or password for the current user. Requires a valid JWT Bearer token."
)
@limiter.limit("5/second")
async def update_profile(
    request: Request,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
        
    return await user_service.update_profile(db, data, current_user)