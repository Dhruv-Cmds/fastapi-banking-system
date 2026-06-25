import os

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import UserRole, hash_password
from app.db.models import User
from app.repository import admin_repository

from dotenv import load_dotenv

load_dotenv()

async def get_all_users(
        db: AsyncSession,
        skip:int,
        limit: int
    ):

    return await admin_repository.get_all_users(
        db,
        skip=skip,
        limit=limit
    )

async def get_all_accounts(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ):

    accounts = await admin_repository.get_all_accounts(
        db,
        skip=skip,
        limit=limit
    )

    return {
        "data": accounts,
        "pagination": {
            "skip": skip,
            "limit": limit
        }
    }

async def create_admin (db: AsyncSession,):

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    existing_admin = await admin_repository.create_admin(db)

    if existing_admin:
        return
    
    admin_user = User(
        username=ADMIN_USERNAME,
        name="Admin",
        password=hash_password(ADMIN_PASSWORD),
        role=UserRole.ADMIN
    )
    try:

        db.add(admin_user)

        await db.commit()

        print(f"✅ Admin user created: {ADMIN_USERNAME}")

    except Exception:
        await db.rollback()
        raise