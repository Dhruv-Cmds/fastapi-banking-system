from fastapi import APIRouter, Depends
import models as models
from fastapi import HTTPException
from db import SessionLocal
from schemas import AccountCreate, Amount, Transfer, UserCreate
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/accounts")
def create_account(account: AccountCreate, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == account.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_acc = models.Account (
        acc_no = account.acc_no,
        balance = account.balance,
        user_id = account.user_id
    )

    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc

@router.get("/accounts")
def get_account(db: Session = Depends(get_db)):
    return db.query(models.Account).all()

@router.post("/accounts/{id}/deposit")
def deposit (id: int, data: Amount, db: Session = Depends(get_db)):

    account = db.query(models.Account).filter(models.Account.id == id).first()

    if not account:
        raise HTTPException (status_code=404, detail="Account not found")
    
    if data.amount < 0:
        raise HTTPException (status_code=400, detail= "Amount must be greater than zero")
    
    account.balance += data.amount

    db.commit()
    db.refresh(account)

    return account

@router.post("/accounts/{id}/withdraw")
def withdraw (id: int, data: Amount, db: Session = Depends(get_db)):

    account = db.query(models.Account).filter(models.Account.id == id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Acoount not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    if data.amount > account.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    account.balance -= data.amount

    db.commit()
    db.refresh(account)

    return account

@router.post("/transfer")
def transfer(data: Transfer, db: Session = Depends(get_db)):

    from_acc = db.query(models.Account).filter(models.Account.id == data.from_account_id).first()
    to_acc = db.query(models.Account).filter(models.Account.id == data.to_account_id).first()

    if not from_acc or not to_acc:
        raise HTTPException (status_code=404, detail= "Account not found")
    
    if from_acc.id == to_acc.id:
        raise HTTPException(status_code=404, detail="Cannot transfer to same account")
    
    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    if from_acc.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    from_acc.balance -= data.amount
    to_acc.balance += data.amount

    db.commit()
    db.refresh(from_acc)
    db.refresh(to_acc)

    return {
        "message": "Transfer successful",
        "from_account_balance": from_acc.balance,
        "to_account_balance": to_acc.balance
    }

@router.post("/test-user")
def test_user(user:UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        username=user.username,
        name= user.name,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "user created"}