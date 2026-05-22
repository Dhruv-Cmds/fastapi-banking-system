from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models import User, Account
from backend.dependencies.db import get_db
from backend.dependencies.auth import get_admin_user
from backend.core import AccountNotFoundError, AccountAlreadyClosedError

router = APIRouter(prefix="/admin", tags=["Admin"])


# View all users
@router.get("/users")
async def get_all_users(
        db: AsyncSession = Depends(get_db),
        admin = Depends(get_admin_user)
    ):
    
    result = await db.execute(select(User))
    users = result.scalars().all()
    return [
        {"id": u.id, "username": u.username, "name": u.name, "role": u.role}
        for u in users
    ]


# View all accounts
@router.get("/accounts")
async def get_all_accounts(
        db: AsyncSession = Depends(get_db),
        admin = Depends(get_admin_user)
    ):

    result = await db.execute(select(Account))
    accounts = result.scalars().all()
    return [
        {"id": a.id, "acc_no": a.acc_no, "balance": a.balance, "status": a.status}
        for a in accounts
    ]


# Close an account
@router.put("/accounts/{account_id}/close")
async def close_account(
        account_id: int,
        db: AsyncSession = Depends(get_db),
        admin = Depends(get_admin_user)
    ):
    result = await db.execute(select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()

    if not account:
        raise AccountNotFoundError()

    if account.status == "CLOSED":
        raise AccountAlreadyClosedError()
    
    # toggle closed
    account.status = "CLOSED"
    await db.commit()

    return {"message": "Account closed successfully"}