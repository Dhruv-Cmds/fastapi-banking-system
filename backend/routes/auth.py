from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db
from backend.schemas import UserCreate, UserLogin, UserUpdate
from backend.services import user_service
from backend.dependencies import get_current_user

router = APIRouter()


# SIGNUP
@router.post("/signup")
async def signup(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.login_user(db, user)


# LOGIN
@router.post("/login")
async def login(
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    return await user_service.signup_user(db, user)


# UPDATE PROFILE
@router.put("/me")
async def update_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await user_service.update_profile(db, data, current_user)

