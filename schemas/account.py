from pydantic import BaseModel

class AccountCreate(BaseModel):

    acc_no: str
    balance: float
    user_id: int

class Amount(BaseModel):

    amount: float

class Transfer(BaseModel):

    from_account_id: int
    to_account_id: int
    amount: int
   