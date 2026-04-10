from pydantic import BaseModel

class AccountCreate(BaseModel):

    name: str
    acc_no: str
    balance: int

class Amount(BaseModel):

    amount: int

class Transfer(BaseModel):

    from_account_id: int
    to_account_id: int
    amount: int