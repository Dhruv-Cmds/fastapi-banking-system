from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from backend.models import Account, Transaction
from backend.core import MAX_DEPOSIT, MAX_WITHDRAW, MAX_TRANSFER


# CREATE
async def create_account(db: AsyncSession, account, current_user):
    result = await db.execute(
        select(Account).where(Account.acc_no == account.acc_no)
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, "Account number already exists")

    new_acc = Account(
        acc_no=account.acc_no,
        balance=0,
        user_id=current_user.id
    )

    db.add(new_acc)
    await db.commit()
    await db.refresh(new_acc)

    return new_acc


# READ
async def get_accounts(db: AsyncSession, current_user):
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )
    return result.scalars().all()


# DEPOSIT
async def deposit(db: AsyncSession, id, data, current_user):
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
        raise HTTPException(404, "Account not found")

    if data.amount > MAX_DEPOSIT:
        raise HTTPException(400, "Deposit limit exceeded")

    acc.balance += data.amount

    db.add(Transaction(
        from_account_id=None,
        to_account_id=acc.id,
        amount=data.amount
    ))

    await db.commit()
    await db.refresh(acc)

    return acc

# WITHDRAW
async def withdraw(db: AsyncSession, id, data, current_user):
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
            raise HTTPException(404, "Account not found")

        if data.amount > MAX_WITHDRAW:
            raise HTTPException(400, "Withdraw limit exceeded")

        if data.amount > acc.balance:
            raise HTTPException(400, "Insufficient balance")

        acc.balance -= data.amount

        db.add(Transaction(
            from_account_id=acc.id,
            to_account_id=None,
            amount=data.amount
        ))

        await db.commit()
        await db.refresh(acc)

        return acc

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Withdraw failed")


# TRANSFER
async def transfer(db: AsyncSession, data, current_user):
    try:
        # Lock sender
        result_from = await db.execute(
            select(Account)
            .where(
                Account.id == data.from_account_id,
                Account.status == "ACTIVE"
            )
            .with_for_update()
        )
        from_acc = result_from.scalar_one_or_none()

        # Lock receiver
        result_to = await db.execute(
            select(Account)
            .where(
                Account.acc_no == data.to_account_no,
                Account.status == "ACTIVE"
            )
            .with_for_update()
        )
        to_acc = result_to.scalar_one_or_none()

        if not from_acc or not to_acc:
            raise HTTPException(404, "Account not found")

        if from_acc.user_id != current_user.id:
            raise HTTPException(403, "Not authorized")

        if from_acc.id == to_acc.id:
            raise HTTPException(400, "Cannot transfer to same account")

        if data.amount > MAX_TRANSFER:
            raise HTTPException(400, "Transfer limit exceeded")

        if from_acc.balance < data.amount:
            raise HTTPException(400, "Insufficient balance")

        # Perform transfer
        from_acc.balance -= data.amount
        to_acc.balance += data.amount

        db.add(Transaction(
            from_account_id=from_acc.id,
            to_account_id=to_acc.id,
            amount=data.amount
        ))

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

    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(500, "Delete failed")