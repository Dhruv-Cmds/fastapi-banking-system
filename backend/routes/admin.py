from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.models import User, Account
from backend.db import get_db
from backend.dependencies.auth import get_admin_user

router = APIRouter(prefix="/api/admin", tags=["Admin"])


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


# Freeze or unfreeze an account
@router.put("/accounts/{account_id}/freeze")
async def freeze_account(
    account_id: int,
    db: AsyncSession = Depends(get_db),
    admin = Depends(get_admin_user)
):
    result = await db.execute(select(Account).where(Account.id == account_id))
    account = result.scalar_one_or_none()

    if not account:
        from fastapi import HTTPException
        raise HTTPException(404, "Account not found")

    # toggle freeze
    account.status = "FROZEN" if account.status == "ACTIVE" else "ACTIVE"
    await db.commit()

    return {"message": f"Account {account.status.lower()}d successfully"}