from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import User, Account
from app.core import UserRole

import os 

from dotenv import load_dotenv

load_dotenv()

from app.core import (
    hash_password, 
)

async def get_all_users(
        db: AsyncSession ,
    ):
    
    result = await db.execute(
        select(User)
    )

    return result.scalars().all()


async def get_all_accounts(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ):

    result = await db.execute(
        select(Account)
        .order_by(Account.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    accounts = result.scalars().all()

    return accounts


async def create_admin (
        db: AsyncSession,
    ):

    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        return 
    
    result = await db.execute(
        select(User)
        .where(User.username == ADMIN_USERNAME)
    )

    existing_admin = result.scalar_one_or_none()

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