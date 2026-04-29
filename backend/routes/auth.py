from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas import UserCreate, UserLogin, UserUpdate
from backend.services import user_service
from backend.dependencies import get_current_user
from backend.dependencies.db import get_db
from backend.core.limiter import limiter

router = APIRouter()


# SIGNUP
@router.post("/signup")
@limiter.limit("3/second")
async def signup(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.signup_user(db, user)


# LOGIN
@router.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.login_user(db, user)


# UPDATE PROFILE
@router.put("/me")
@limiter.limit("5/second")
async def update_profile(
    request: Request,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return await user_service.update_profile(db, data, current_user)