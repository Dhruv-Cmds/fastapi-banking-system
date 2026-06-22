from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api import get_db, get_current_user

from app.schemas import (
    AccountCreate,
    Amount,
    Transfer,
    AccountResponse,
    UserResponse,
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
@limiter.limit("5/second")
async def create_account(
        request: Request,
        account: AccountCreate,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await account_service.create_account(db, account, current_user)


# GET USER ACCOUNTS
@router.get(
    "/accounts",
    response_model=List[AccountResponse],
    summary="List authenticated user accounts",
    description="Return all accounts owned by the current user. Requires JWT Bearer authentication."
)
@limiter.limit("20/second")
async def get_accounts(
        request: Request,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await account_service.get_accounts(db, current_user)


# DEPOSIT
@router.post(
    "/accounts/{id}/deposit",
    response_model=UserResponse,
    summary="Deposit funds to an account",
    description="Deposit money into an active account owned by the authenticated user."
)
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
@router.post(
    "/accounts/{id}/withdraw",
    response_model=UserResponse,
    summary="Withdraw funds from an account",
    description="Withdraw money from an active account owned by the authenticated user, if sufficient balance exists."
)
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
@router.post(
    "/transfer",
    response_model=UserResponse,
    summary="Transfer funds between accounts",
    description=(
        "Transfer funds from one owned account to another active account. "
        "Self-transfers are prevented and account ownership is validated."
    )
)
@limiter.limit("3/second")
async def transfer(
        request: Request,
        data: Transfer,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):

    return await account_service.transfer(db, data, current_user)

@router.get(
    "/transactions/{account_id}",
    response_model=TransactionListResponse,
    summary="List account transactions",
    description="Return transaction history for a specific account owned by the authenticated user."
)
async def get_transactions(
        request: Request,
        account_id: int,
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
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
@limiter.limit("2/second")
async def delete_account(
        request: Request,
        account_id: int,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
    ):
    
    return await account_service.delete_account(
        db, 
        current_user,
        account_id=account_id,
    )