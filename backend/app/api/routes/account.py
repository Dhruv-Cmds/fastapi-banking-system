from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import get_db, get_current_user

from app.schemas import (
    AccountCreate,
    MoneyRequest,
    Transfer,
    TransferRequest,
    AccountResponse,
    Balance,
    TransactionListResponse,
)

from app.services import account_service
from app.core import limiter


router = APIRouter(tags=["Accounts"])


# CREATE ACCOUNT
@router.post(
    "/accounts",
    response_model=AccountResponse,
    summary="Open a new account",
    description="Create a new account for the authenticated user. Initial balance is always zero."
)
@limiter.limit("5/minute")
async def create_account(
        request: Request,
        account: AccountCreate,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.create_account(db, account, current_user)


# GET USER ACCOUNTS
@router.get(
    "/accounts",
    response_model=List[AccountResponse],
    summary="List authenticated user accounts",
    description="Return all accounts owned by the current user. Requires JWT Bearer authentication."
)
@limiter.limit("60/minute")
async def get_accounts(
        request: Request,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.get_accounts(db, current_user)


# DEPOSIT
@router.post(
    "/accounts/{account_id}/deposit",
    response_model=AccountResponse,
    summary="Deposit funds to an account",
    description="Deposit money into an active account owned by the authenticated user."
)
@limiter.limit("2/10second;10/minute")
async def deposit(
        request: Request,
        account_id: int,
        deposite: MoneyRequest,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.deposit(db, account_id, deposite.amount, current_user)


# WITHDRAW
@router.post(
    "/accounts/{account_id}/withdraw",
    response_model=AccountResponse,
    summary="Withdraw funds from an account",
    description="Withdraw money from an active account owned by the authenticated user, if sufficient balance exists."
)
@limiter.limit("1/10second;5/minute")
async def withdraw(
        request: Request,
        account_id: int,
        withdraw: MoneyRequest,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.withdraw(db, account_id, withdraw.amount, current_user)


# TRANSFER
@router.post(
    "/transfer",
    response_model=TransferRequest,
    summary="Transfer funds between accounts",
    description=(
        "Transfer funds from one owned account to another active account. "
        "Self-transfers are prevented and account ownership is validated."
    )
)
@limiter.limit("1/10second;5/minute")
async def transfer(
        request: Request,
        data: Transfer,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.transfer(db, data, current_user)

@router.get(
    "/transactions/{account_id}",
    response_model=TransactionListResponse,
    summary="List account transactions",
    description="Return transaction history for a specific account owned by the authenticated user."
)
@limiter.limit("10/second;120/minute")
async def get_transactions(
        request: Request,
        account_id: int,
        skip: int=Query(0, ge=0),
        limit: int=Query(20, ge=1, le=100),
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):  
    
    transactions =  await account_service.get_transactions(
            db, 
            account_id, 
            current_user, 
            skip=skip, 
            limit=limit
        )

    return {
        "data":transactions,  
        "pagination": {
            "skip": skip,
            "limit": limit
        }
    }
    

# SHOW ACCOUNT BALANCE
@router.post(
    "/accounts/{account_number}",
    response_model=Balance,
    summary="Check Account balance",
    description=(
        "Only authenticated user can see only their account(s) balance"
    )
)
@limiter.limit("1/10second")
async def get_account_balance(
        request: Request,
        account_number: int, 
        pin: str,  
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):

    return await account_service.get_account_balance(
        db,
        account_number,
        pin,
        current_user
    )

# DELETE (CLOSE ACCOUNT)
@router.delete(
    "/accounts/{account_id}",
    response_model=AccountResponse,
    summary="Close an account",
    description=(
        "Soft-close an account owned by the authenticated user. "
        "Only accounts with zero balance can be closed."
    )
)
@limiter.limit("1/minute")
async def delete_account(
        request: Request,
        account_id: int,
        db: AsyncSession=Depends(get_db),
        current_user=Depends(get_current_user)
    ):
    
    return await account_service.delete_account(
        db, 
        current_user,
        account_id=account_id,
    )