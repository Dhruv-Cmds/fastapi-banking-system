from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db, get_current_user
from backend.schemas import AccountCreate, Amount, Transfer
from backend.services import account_service
from backend.core.limiter import limiter


router = APIRouter()


# CREATE ACCOUNT
@router.post("/accounts")
@limiter.limit("5/second")
async def create_account(
    request: Request,
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.create_account(db, account, current_user)


# GET USER ACCOUNTS
@router.get("/accounts")
@limiter.limit("20/second")
async def get_accounts(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.get_accounts(db, current_user)


# DEPOSIT
@router.post("/accounts/{id}/deposit")
@limiter.limit("10/second")
async def deposit(
    request: Request,
    id: int,
    data: Amount,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.deposit(db, id, data, current_user)


# WITHDRAW
@router.post("/accounts/{id}/withdraw")
@limiter.limit("5/second")
async def withdraw(
    request: Request,
    id: int,
    data: Amount,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.withdraw(db, id, data, current_user)


# TRANSFER
@router.post("/transfer")
@limiter.limit("3/second")
async def transfer(
    request: Request,
    data: Transfer,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.transfer(db, data, current_user)


# DELETE (CLOSE ACCOUNT)
@router.delete("/accounts/{id}")
@limiter.limit("2/second")
async def delete_account(
    request: Request,
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.delete_account(db, id, current_user)