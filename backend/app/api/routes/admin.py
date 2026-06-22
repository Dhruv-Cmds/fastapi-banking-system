from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core import limiter

from app.api import get_db, get_admin_user

from app.schemas import UserResponse, AccountListResponse
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["Admin"])


# View all users
@router.get(
        "/users",
        response_model=List[UserResponse],
        summary="Get all users",
        description="Retrive all registered users. Only admin can access"
    )
@limiter.limit("30/minute")
async def get_all_users(
        request: Request,
        db: AsyncSession = Depends(get_db),
        admin = Depends(get_admin_user)
    ):
    
        return admin_service.get_all_users(db)


# View all accounts
@router.get(
        "/accounts",
        response_model=List[AccountListResponse],
        summary="Get all users accounts",
        description="Retrive all registered users accounts. Only admin can access"
    )
@limiter.limit("30/minute")
async def get_all_accounts(
        request: Request,
        db: AsyncSession = Depends(get_db),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=0, le=100),
        admin = Depends(get_admin_user),
    ):

    return await admin_service.get_all_accounts(
        db, 
        skip=skip,
        limit=limit
    )
