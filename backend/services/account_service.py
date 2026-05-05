from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from backend.models import Account, Transaction
from backend.core import MAX_DEPOSIT, MAX_WITHDRAW, MAX_TRANSFER


# CREATE
async def create_account(db: AsyncSession, account, current_user):

    new_acc = Account(
        acc_no=account.acc_no,
        balance=0,
        user_id=current_user.id
    )

    try:
        db.add(new_acc)
        await db.commit()
        await db.refresh(new_acc) 

        return new_acc

    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Account number already exists")


# READ
async def get_accounts(db: AsyncSession, current_user):
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )
    return result.scalars().all()


# DEPOSIT
async def deposit(db: AsyncSession, id, data, current_user):

    try:

        if data.amount > MAX_DEPOSIT:
            raise HTTPException(400, "Deposit limit exceeded")

        result = await db.execute(
            update(Account)
            .where(
                Account.id == id,
                Account.user_id == current_user.id,
                Account.status == "ACTIVE"
            )
            .values(balance=Account.balance + data.amount)
            .execution_options(synchronize_session="fetch")
        )

        if result.rowcount == 0:
            raise HTTPException(404, "Account not found")

        db.add(Transaction(
            from_account_id=None,
            to_account_id=id,
            amount=data.amount
        ))

        await db.commit()

        return {"message": "Deposit successful"}

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Deposit failed")


# WITHDRAW
async def withdraw(db: AsyncSession, id, data, current_user):

    try:

        if data.amount > MAX_WITHDRAW:
            raise HTTPException(400, "Withdraw limit exceeded")

        result = await db.execute(
            update(Account)
            .where(
                Account.id == id,
                Account.user_id == current_user.id,
                Account.status == "ACTIVE",
                Account.balance >= data.amount
            )
            .values(balance=Account.balance - data.amount)
            .execution_options(synchronize_session="fetch")  # ✅ FIX
        )

        if result.rowcount == 0:
            raise HTTPException(400, "Insufficient balance or account not found")

        db.add(Transaction(
            from_account_id=id,
            to_account_id=None,
            amount=data.amount
        ))

        await db.commit()

        return {"message": "Withdraw successful"}

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Withdraw failed")


# TRANSFER
# TRANSFER
async def transfer(db: AsyncSession, data, current_user):

    try:

        if data.amount > MAX_TRANSFER:
            raise HTTPException(400, "Transfer limit exceeded")

        query_from = select(Account).where(
            Account.id == data.from_account_id,
            Account.user_id == current_user.id,
            Account.status == "ACTIVE"
        ).with_for_update()

        query_to = select(Account).where(
            Account.acc_no == data.to_account_no,
            Account.status == "ACTIVE"
        ).with_for_update()

        result_from = await db.execute(query_from)
        from_acc = result_from.scalar_one_or_none()

        result_to = await db.execute(query_to)
        to_acc = result_to.scalar_one_or_none()

        if not from_acc or not to_acc:
            raise HTTPException(404, "Account not found")

        if from_acc.balance < data.amount:
            raise HTTPException(400, "Insufficient balance")

        # perform transfer safely
        from_acc.balance -= data.amount
        to_acc.balance += data.amount

        db.add(Transaction(
            from_account_id=from_acc.id,
            to_account_id=to_acc.id,
            amount=data.amount
        ))

        await db.commit()

        return {"message": "Transfer successful"}

    except HTTPException:
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Transfer failed")


# DELETE ACCOUNT
async def delete_account(db: AsyncSession, id, current_user):

    try:

        result = await db.execute(
            select(Account)
            .where(Account.id == id)
            .with_for_update()
        )

        acc = result.scalar_one_or_none()

        if not acc:
            raise HTTPException(404, "Account not found")

        if acc.user_id != current_user.id:
            raise HTTPException(403, "Not authorized")

        if acc.status == "CLOSED":
            raise HTTPException(400, "Account already closed")

        if acc.balance != 0:
            raise HTTPException(400, "Balance must be zero")

        acc.status = "CLOSED"

        await db.commit()

        return {"message": "Account closed successfully"}

    except HTTPException:
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Delete failed")
