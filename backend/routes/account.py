from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User, Account, Transaction
from backend.schemas import AccountCreate, Amount, Transfer
from backend.dependencies import get_current_user
from backend.db import get_db

from backend.core import MAX_DEPOSIT, MAX_WITHDRAW, MAX_TRANSFER

router = APIRouter()


# CREATE ACCOUNT
@router.post("/accounts",)
async def create_accounts (
                account: AccountCreate, 
                db: AsyncSession = Depends(get_db), 
                current_user: User = Depends(get_current_user)
    ):

    try:

         # Check duplicate account number   
        result = await db.execute(
            select(Account).where(Account.acc_no == account.acc_no)
        )

        existing = result.scalar_one_or_none()

        if existing:
            raise HTTPException(status_code=400, detail="Account number already exists")

        new_acc = Account(
            acc_no=account.acc_no,
            balance=0,
            user_id= current_user.id
        )

        db.add(new_acc)
        await db.commit()
        await db.refresh(new_acc)

        return new_acc

    except SQLAlchemyError:

        await db.rollback()
        raise HTTPException(status_code=500, detail="Account creation failed")


#  GET USER ACCOUNTS
@router.get("/accounts")
async def get_account(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
    ):

    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )

    return result.scalar().all()


# DEPOSIT
@router.post("/accounts/{id}/deposit")
async def deposit(
            id: int, 
            data: Amount, 
            db: AsyncSession = Depends(get_db), 
            current_user: User = Depends(get_current_user)
    ):

    try:
        result = await db.execute(
            select(Account)
            .where(
                Account.id == id,
                Account.user_id == current_user.id,
                Account.status == "ACTIVE"
            )
            .with_for_update()
        )

        acc = result.scalar_one_or_none()

        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")
        
        
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

        await db.commit()
        await db.refresh(acc)

        return acc
    
    except SQLAlchemyError:

        await db.rollback()
        raise HTTPException (status_code=500, detail="Deposit failed")


# WITHDRAW
@router.post("/accounts/{id}/withdraw")
async def withdraw(

            id: int, 
            data: Amount, 
            db: AsyncSession = Depends(get_db), 
            current_user: User = Depends(get_current_user)
    ):

    try:
        result = await db.execute(
            select(Account)
            .where(
                Account.id == id,
                Account.user_id == current_user.id,
                Account.status == "ACTIVE"
            )
            .with_for_update()
        )

        acc = result.scalar_one_or_none()
        
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

        await db.commit()
        await db.refresh(acc)

        return acc
    
    except SQLAlchemyError:
        
        await db.rollback()
        raise HTTPException (status_code=500, detail="Withdrawn failed")


# TRANSFER 
@router.post("/transfer")
async def transfer(
        data: Transfer, 
        db: AsyncSession = Depends(get_db), 
        current_user: User = Depends(get_current_user)
    ):

    # with_for_update() = " This row and nobody else can touch it until I'm done."

    try:
        
        result_from  = await db.execute(
            select(Account)
            .where(
                Account.id == data.from_account_id, 
                Account.status == "ACTIVE"
            )
            .with_for_update()     
        )

        from_acc = result_from.scalar_one_or_none()

        result_to  = db.execute(
            select(Account)
            .where(
                Account.acc_no == data.to_account_no, 
                Account.status == "ACTIVE"
            )
            .with_for_update()
        )
        
        to_acc = result_to.scalar_one_or_none()

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

        await db.commit()

        await db.refresh(from_acc)
        await db.refresh(to_acc)

        return {
            "message": "Transfer successful",
            "from_account_balance": from_acc.balance,
            "to_account_balance": to_acc.balance
        }

    except SQLAlchemyError:

        await db.rollback()
        raise HTTPException (status_code=500, detail="Transfer failed")


# DELETE   
@router.delete("/accounts/{id}")
async def delete_account(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    try:
    
        result = await db.execute(
            select(Account)
            .where(Account.id == id)
            .with_for_update()
        )

        acc = result.scalar_one_or_none()

        if not acc:
            raise HTTPException(status_code=404, detail="Account not found")

        if acc.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized")

        if acc.status == "CLOSED":
            raise HTTPException(status_code=400, detail="Account already closed")

        if acc.balance != 0:
            raise HTTPException(status_code=400, detail="Balance must be zero")

        acc.status = "CLOSED"

        await db.commit()

        return {"message": "Account closed successfully"}
    
    except SQLAlchemyError:

        await db.rollback()
        raise HTTPException(status_code=500, detail="Something went wrong")