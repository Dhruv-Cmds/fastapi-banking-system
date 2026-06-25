import os 

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import User, Account

from dotenv import load_dotenv

load_dotenv()

async def get_all_users(
        db: AsyncSession,
        skip:int = 0,
        limit:int = 100
    ):
    
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(skip)
        .limit(limit)
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
    return result.scalars().all()


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

    return result.scalar_one_or_none()
