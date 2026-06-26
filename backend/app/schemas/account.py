from pydantic import BaseModel, Field

from decimal import Decimal

from typing import Optional, List

from app.core import AccountStatus

class PaginationMeta(BaseModel):
    skip: int
    limit: int

class AccountCreate(BaseModel):
    acc_no: int = Field(
        ..., 
        gt=0, 
        examples=[1001], 
    )
    balance: Decimal = Field(
        default=0, 
        examples=[0], 
    )


class Transfer(BaseModel):
    from_account_id: int = Field(..., gt=0, examples=[1])
    to_account_id: int = Field(..., gt=0, examples=[2])
    amount: Decimal = Field(
        ..., 
        gt=0, 
        max_digits=12, 
        decimal_places=2, 
        example=50.00
    )
    
    model_config = {
        "from_attributes": True
    }


class TransferRequest(BaseModel):
    from_account_id: int = Field(..., gt=0, examples=[1])
    to_account_id: int = Field(..., gt=0, examples=[2])
    amount: Decimal = Field(
        ..., 
        gt=0, 
        max_digits=12, 
        decimal_places=2, 
        example=50.00
    )
    message: str

    model_config = {
        "from_attributes": True
    }


class AccountResponse(BaseModel):
    id: int = Field(..., examples=[1])
    acc_no: int = Field(..., gt=0, examples=[1001])
    balance: Decimal = Field(..., examples=[6999.34])
    status: AccountStatus = Field(..., examples=[AccountStatus.ACTIVE])
    user_id: int = Field(..., examples=[1])

    model_config = {
        "from_attributes":True,
    }

class AccountListResponse(BaseModel):
    data: List[AccountResponse]
    pagination: PaginationMeta


class TransactionResponse(BaseModel):
    id: int
    amount: float

    from_account_id: Optional[int]
    to_account_id: Optional[int]

    model_config = {
        "from_attributes":True
    }


class TransactionListResponse(BaseModel):
    data: List[TransactionResponse]
    pagination: PaginationMeta