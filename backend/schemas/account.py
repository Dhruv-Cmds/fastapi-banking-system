from pydantic import BaseModel, Field

from decimal import Decimal

from datetime import datetime

from typing import Optional, List


# CREATE ACCOUNT
class AccountCreate(BaseModel):

    acc_no: int = Field(..., gt=0, example=1001, description="Unique account number")
    balance: Decimal = Field(default=0, example=0, description="Balance starts at zero")


# DEPOSIT / WITHDRAW
class Amount(BaseModel):

    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2, example=150.00)


# TRANSFER
class Transfer(BaseModel):

    from_account_id: int = Field(..., gt=0, example=1)
    to_account_no: int = Field(..., gt=0, example=2002)
    amount: Decimal = Field(..., gt=0, max_digits=12, decimal_places=2, example=50.00)


class AccountResponse(BaseModel):
    id: int
    acc_no: int
    balance: Decimal
    status: str
    user_id: int

    class Config:
        orm_mode = True


class TransactionResponse(BaseModel):
    id: int
    # type: str
    amount: float

    from_account_id: Optional[int]
    to_account_id: Optional[int]

    created_at: datetime

    class Config:
        from_attributes = True

class TransactionListResponse(BaseModel):
    data: List[TransactionResponse]
    skip: int
    limit: int