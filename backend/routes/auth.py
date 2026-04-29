from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db, get_current_user 
from backend.models import User
from backend.schemas import UserCreate, UserLogin, UserUpdate
from backend.core import hash_password, verify_password, create_access_token

router = APIRouter()


# SIGNUP
@router.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):

    try:
        
        # Case-insensitive username check
        result = await db.execute(
            select(User)
            .where(
            func.lower(User.username) == user.username.lower()
            )
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        new_user = User(
            username=user.username.lower(),
            name=user.name,
            password=hash_password(user.password)
        )


        db.add(new_user)
        
        await db.commit()

        await db.refresh(new_user)

        return {"message": "User created"}

    except SQLAlchemyError:

        await db.rollback()

        raise HTTPException(status_code=500, detail="Signup failed")


# LOGIN
@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):

    try:

        # Case-insensitive lookup
        result = await db.execute(
            select(User)
            .where(
            func.lower(User.username) == user.username.lower())
        )

        db_user = result.scalar_one_or_none()


        # Do NOT reveal whether user exists or password is wrong
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        #  Create JWT token
        token = create_access_token({
            "sub": str(db_user.id)
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Login failed")

#  UPDATE PROFILE
@router.put("/me")
async def update_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    
    try:

        #  Update only allowed fields
        if data.name:
            current_user.name = data.name

        if data.password:
            current_user.password = hash_password(data.password)


        db.commit()
        
        await db.refresh(current_user)


        return {"message": "Profile updated"}
    
    
    except SQLAlchemyError:

        await db.rollback()
        raise HTTPException(500, "Update failed")