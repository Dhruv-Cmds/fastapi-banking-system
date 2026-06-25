from sqlalchemy import or_, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account, Transaction, User
from app.schemas import Transfer

async def get_accounts_by_user_id(
        db: AsyncSession, 
        user_id: int
    ):

    result = await db.execute(
        select(Account)
        .where(Account.user_id == user_id)
    )
    return result.scalars().all()


async def get_owned_account(
        db: AsyncSession, 
        account_id: int, 
        current_user: User
    ):
    
    result = await db.execute(
        select(Account)
        .where(
            and_(
                (Account.id == account_id),
                (Account.user_id == current_user.id)
            )
        )
        .with_for_update()
    )
    return result.scalar_one_or_none()


async def get_account(
        db: AsyncSession, 
        account_id: int, 
    ):
    
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .with_for_update()
    )
    return result.scalar_one_or_none()


async def get_accounts_for_transfer(
        db: AsyncSession, 
        data: Transfer
    ):
    
    result = await db.execute(
            select(Account)
            .where(
                or_(
                    (Account.id == data.from_account_id),
                    (Account.acc_no == data.to_account_no)
                )
            )
            .order_by(Account.id)
            .with_for_update()
        )
    return result.scalars().all()

async def get_transactions(
        db: AsyncSession,
        account_id,
        skip,
        limit
    ):

    txn_query = await db.execute(
            select(Transaction)
            .where(
                or_(
                    (Transaction.from_account_id == account_id),
                    (Transaction.to_account_id == account_id)
                )
            )
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
    return txn_query.scalars().all()