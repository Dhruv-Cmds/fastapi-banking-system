from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_db, get_current_user
from backend.schemas import AccountCreate, Amount, Transfer
from backend.services import account_service

router = APIRouter()


# CREATE ACCOUNT
@router.post("/accounts")
async def create_account(
    account: AccountCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.create_account(db, account, current_user)


# GET USER ACCOUNTS
@router.get("/accounts")
async def get_accounts(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.get_accounts(db, current_user)


# DEPOSIT
@router.post("/accounts/{id}/deposit")
async def deposit(
    id: int,
    data: Amount,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.deposit(db, id, data, current_user)


# WITHDRAW
@router.post("/accounts/{id}/withdraw")
async def withdraw(
    id: int,
    data: Amount,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.withdraw(db, id, data, current_user)


# TRANSFER
@router.post("/transfer")
async def transfer(
    data: Transfer,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.transfer(db, data, current_user)


# DELETE (CLOSE ACCOUNT)
@router.delete("/accounts/{id}")
async def delete_account(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await account_service.delete_account(db, id, current_user)