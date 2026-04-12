from pydantic import BaseModel

class AccountCreate(BaseModel):

    acc_no: str
    balance: int
    user_id: int

class Amount(BaseModel):

    amount: int

class Transfer(BaseModel):

    from_account_id: int
    to_account_id: int
    amount: int

class UserCreate(BaseModel):

    username: str
    name: str
    password: str    