from pydantic import BaseModel
from decimal import Decimal

class AccountCreate(BaseModel):

    acc_no: int
    balance: Decimal

# For deposit and withdraw
class Amount(BaseModel):

    amount: Decimal

# For transfer 
class Transfer(BaseModel):

    from_account_id: int
    to_account_no: int
    amount: Decimal
   
