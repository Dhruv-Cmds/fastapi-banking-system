from pydantic import BaseModel, Field

from decimal import Decimal

from typing import Optional, List

from app.core import UserStatus

class PaginationMeta(BaseModel):
    skip: int
    limit: int

class AccountCreate(BaseModel):
    acc_no: int = Field(
        ..., 
        gt=0, 
        example=[1001], 
        description="Unique account number"
    )
    balance: Decimal = Field(
        default=0, 
        example=[0], 
        description="Balance starts at zero"
    )


# DEPOSIT / WITHDRAW
class Amount(BaseModel):
    amount: Decimal = Field(
        ..., 
        gt=0, 
        max_digits=12, 
        decimal_places=2, 
        example=[150.00]
    )

class Transfer(BaseModel):
    from_account_id: int = Field(..., gt=0, example=1)
    to_account_no: int = Field(..., gt=0, example=[2002])
    amount: Decimal = Field(
        ..., 
        gt=0, 
        max_digits=12, 
        decimal_places=2, 
        example=[50.00]
    )

class AccountResponse(BaseModel):
    id: int = Field(..., examples=[1])
    acc_no: int = Field(..., gt=0, example=[1001])
    balance: Decimal = Field(..., gt=0, examples=[6999.34])
    status: UserStatus = Field(..., examples=[UserStatus.ACTIVE])
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