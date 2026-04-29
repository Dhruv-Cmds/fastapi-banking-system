# backend/services/user_service.py

from sqlalchemy import select, func
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User
from backend.core import hash_password, verify_password, create_access_token


async def signup_user(db: AsyncSession, user):
    result = await db.execute(
        select(User).where(func.lower(User.username) == user.username.lower())
    )

    if result.scalar_one_or_none():
        raise HTTPException(400, "Username already exists")

    new_user = User(
        username=user.username.lower(),
        name=user.name,
        password=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User created"}


async def login_user(db: AsyncSession, user):
    result = await db.execute(
        select(User).where(func.lower(User.username) == user.username.lower())
    )

    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(400, "Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from backend.core import hash_password


async def update_profile(db: AsyncSession, data, current_user):
    try:
        # Update allowed fields
        if data.name:
            current_user.name = data.name

        if data.password:
            current_user.password = hash_password(data.password)

        await db.commit()
        await db.refresh(current_user)

        return {"message": "Profile updated"}

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Update failed")