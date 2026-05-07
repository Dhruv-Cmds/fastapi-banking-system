from pydantic import BaseModel, Field

from decimal import Decimal

from datetime import datetime

from typing import Optional, List


# CREATE ACCOUNT
class AccountCreate(BaseModel):

    acc_no: int = Field(gt=0)              # must be > 0
    balance: Decimal = Field(default=0)    # must be = 0


# DEPOSIT / WITHDRAW
class Amount(BaseModel):

    amount: Decimal = Field(gt=0, max_digits=12, decimal_places=2)        # must be > 0


# TRANSFER
class Transfer(BaseModel):

    from_account_id: int = Field(gt=0)
    to_account_no: int = Field(gt=0)
    amount: Decimal = Field(gt=0)




class TransactionResponse(BaseModel):
    id: int
    type: str
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