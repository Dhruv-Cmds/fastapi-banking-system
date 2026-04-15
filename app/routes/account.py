from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User, Account
from app.schemas import AccountCreate, Amount, Transfer
from app.dependencies import get_current_user
from app.db import get_db

router = APIRouter()


@router.post("/accounts")
def create_accounts (account: AccountCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):


    new_acc = Account(
        acc_no=account.acc_no,
        balance=account.balance,
        user_id= current_user.id
    )

    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc

@router.get("/accounts")
def get_account(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Account).filter(Account.user_id == current_user.id).all()

@router.post("/accounts/{id}/deposit")
def deposit(id: int, data: Amount, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    acc = db.query(Account).filter(Account.id == id).first()

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if acc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    acc.balance += data.amount

    db.commit()
    db.refresh(acc)

    return acc

@router.post("/accounts/{id}/withdraw")
def withdraw(id: int, data: Amount, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    acc = db.query(Account).filter(Account.id == id).first()

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if acc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if data.amount > acc.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    acc.balance -= data.amount

    db.commit()
    db.refresh(acc)

    return acc

@router.post("/transfer")
def transfer(data: Transfer, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # with_for_update() = "I'm reading this row and nobody else can touch it until I'm done."

    # Request 1                          Request 2
    # ─────────────────────────────────────────────────────
    # reads + LOCKS balance = 1000       tries to read...
    # checks: 1000 >= 800 ✅             🔒 WAITING for lock
    # balance -= 800 → writes 200        
    # db.commit() → lock released        reads balance = 200
    #                                 checks: 200 >= 800 ❌
    #                                 returns "Insufficient balance"

    # -------------------------------------------------------------------------------------------------------------------------

    from_acc = db.query(Account).filter(Account.id == data.from_account_id).with_for_update().first()
    to_acc = db.query(Account).filter(Account.id == data.to_account_id).with_for_update().first()

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    if from_acc.id == to_acc.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if from_acc.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    try:
        from_acc.balance -= data.amount
        to_acc.balance += data.amount
        db.commit()

    except:
        db.rollback()
        raise HTTPException (status_code=500, detail="Transfer failed")

    db.refresh(from_acc)
    db.refresh(to_acc)

    return {
        "message": "Transfer successful",
        "from_account_balance": from_acc.balance,
        "to_account_balance": to_acc.balance
    }
