from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models import User, Account, Transaction
from app.schemas import AccountCreate, Amount, Transfer
from app.dependencies import get_current_user
from app.db import get_db

from app.core import MAX_DEPOSIT, MAX_WITHDRAW, MAX_TRANSFER

router = APIRouter()


# CREATE ACCOUNT
@router.post("/accounts",)
def create_accounts (
                account: AccountCreate, 
                db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)
    ):

    try:

         # Check duplicate account number   
        existing = db.query(Account).filter(Account.acc_no == account.acc_no).first()

        if existing:
            raise HTTPException(status_code=400, detail="Account number already exists")

        new_acc = Account(
            acc_no=account.acc_no,
            balance=0,
            user_id= current_user.id
        )

        db.add(new_acc)
        db.commit()
        db.refresh(new_acc)

        return new_acc

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Account creation failed")


#  GET USER ACCOUNTS
@router.get("/accounts")
def get_account(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):

    return db.query(Account).filter(Account.user_id == current_user.id).all()


# DEPOSIT
@router.post("/accounts/{id}/deposit")
def deposit(
            id: int, 
            data: Amount, 
            db: Session = Depends(get_db), 
            current_user: User = Depends(get_current_user)
    ):

    try:

        #  Lock account row
        acc = db.query(Account)\
            .filter(Account.id == id, Account.user_id == current_user.id, Account.status == "ACTIVE")\
            .with_for_update()\
            .first()

        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Removed duplicate amount <= 0 check (handled by schema)
        
        if data.amount > MAX_DEPOSIT:
            raise HTTPException(status_code=400, detail="Deposit limit exceeded")

        acc.balance += data.amount


        #  Audit log
        txn = Transaction(
            from_account_id=None,
            to_account_id=acc.id,
            amount=data.amount
        )

        db.add(txn)

        db.commit()
        db.refresh(acc)

        return acc
    
    except SQLAlchemyError:

        db.rollback()
        raise HTTPException (status_code=500, detail="Deposit failed")


# WITHDRAW
@router.post("/accounts/{id}/withdraw")
def withdraw(

            id: int, 
            data: Amount, 
            db: Session = Depends(get_db), 
            current_user: User = Depends(get_current_user)
    ):

    try:

        #  Lock account row
        acc = db.query(Account)\
            .filter(Account.id == id, Account.user_id == current_user.id, Account.status == "ACTIVE")\
            .with_for_update()\
            .first()
        
        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Removed duplicate amount <= 0 check
        
        if data.amount > MAX_WITHDRAW:
            raise HTTPException(status_code=400, detail="Withdraw limit exceeded")

        if data.amount > acc.balance:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        acc.balance -= data.amount

        # Audit log
        txn = Transaction(
            from_account_id=acc.id,
            to_account_id=None,
            amount=data.amount
        )

        db.add(txn)

        db.commit()
        db.refresh(acc)


        return acc
    
    except SQLAlchemyError:
        
        db.rollback()
        raise HTTPException (status_code=500, detail="Withdrawn failed")


# TRANSFER 
@router.post("/transfer")
def transfer(
        data: Transfer, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(get_current_user)
    ):

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
    try:
        
        # Lock sender
        from_acc = db.query(Account)\
            .filter(Account.id == data.from_account_id, Account.status == "ACTIVE")\
            .with_for_update()\
            .first()
        
        # Lock receiver
        to_acc = db.query(Account)\
            .filter(Account.acc_no == data.to_account_no, Account.status == "ACTIVE")\
            .with_for_update()\
            .first()

        if not from_acc or not to_acc:
            raise HTTPException(status_code=404, detail="Account not found")
        

        if from_acc.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        

        if from_acc.id == to_acc.id:
            raise HTTPException(status_code=400, detail="Cannot transfer to same account")
        

        # FIXED: correct transfer limit logic
        if data.amount > MAX_TRANSFER:
            raise HTTPException(status_code=400, detail="Transfer limit exceeded")
        

        if from_acc.balance < data.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
 

        # Perform transfer
        from_acc.balance -= data.amount
        to_acc.balance += data.amount
        

        # Audit log
        txn = Transaction(
                    from_account_id=from_acc.id,
                    to_account_id=to_acc.id,
                    amount=data.amount
                )
        

        db.add(txn)

        db.commit()

        db.refresh(from_acc)
        db.refresh(to_acc)

        return {
            "message": "Transfer successful",
            "from_account_balance": from_acc.balance,
            "to_account_balance": to_acc.balance
        }
    
    except Exception as e:
        db.rollback()
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

    except SQLAlchemyError:

        # db.rollback()
        raise HTTPException (status_code=500, detail="Transfer failed")


# DELETE   
@router.delete("/accounts/{id}")
def delete_account(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
    
        acc = db.query(Account)\
            .filter(Account.id == id)\
            .first()

        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")

        if acc.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

        if acc.status == "CLOSED":
            raise HTTPException(status_code=400, detail="Account already closed")

        if acc.balance != 0:
            raise HTTPException(status_code=400, detail="Balance must be zero")

        acc.status = "CLOSED"

        db.commit()

        return {"message": "Account closed successfully"}
    
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong")