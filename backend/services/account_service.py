from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from backend.models import Account, Transaction

from backend.core import (
    MAX_DEPOSIT, 
    MAX_WITHDRAW, 
    MAX_TRANSFER,
    AccountAlreadyExistsError,
    AccountNotFoundError,
    AccountInactiveError,
    DepositLimitExceededError,
    WithdrawLimitExceededError,
    TransferLimitExceededError,
    InsufficientFundsError,
    UnauthorizedAccessError,
    AccountAlreadyClosedError,
    NonZeroBalanceError,
    DatabaseError,
)


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
        raise AccountAlreadyExistsError()


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
            raise DepositLimitExceededError()

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
            raise AccountNotFoundError()

        db.add(Transaction(
            from_account_id=None,
            to_account_id=id,
            amount=data.amount,
            status="SUCCESS"
        ))

        await db.commit()

        return {"message": "Deposit successful"}

    except (DepositLimitExceededError, AccountNotFoundError):
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Deposit operation")


# WITHDRAW
async def withdraw(db: AsyncSession, id, data, current_user):

    try:

        if data.amount > MAX_WITHDRAW:
            raise WithdrawLimitExceededError()

        result = await db.execute(
            update(Account)
            .where(
                Account.id == id,
                Account.user_id == current_user.id,
                Account.status == "ACTIVE",
                Account.balance >= data.amount
            )
            .values(balance=Account.balance - data.amount)
            .execution_options(synchronize_session="fetch")
        )

        if result.rowcount == 0:
            raise InsufficientFundsError("Insufficient balance or account not found")

        db.add(Transaction(
            from_account_id=id,
            to_account_id=None,
            amount=data.amount,
            status="SUCCESS"
        ))

        await db.commit()

        return {"message": "Withdraw successful"}

    except (WithdrawLimitExceededError, InsufficientFundsError):
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Withdrawal operation")


# TRANSFER
async def transfer(db: AsyncSession, data, current_user):

    try:

        if data.amount > MAX_TRANSFER:
            raise TransferLimitExceededError()

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
            raise AccountNotFoundError()

        if from_acc.balance < data.amount:
            raise InsufficientFundsError()

        # perform transfer safely
        from_acc.balance -= data.amount
        to_acc.balance += data.amount

        db.add(Transaction(
            from_account_id=from_acc.id,
            to_account_id=to_acc.id,
            amount=data.amount,
            status="SUCCESS"
        ))

        await db.commit()

        return {"message": "Transfer successful"}

    except (TransferLimitExceededError, AccountNotFoundError, InsufficientFundsError):
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Transfer operation")
    
async def get_transactions(
        db: AsyncSession,
        account_id: int,
        current_user,
        skip: int = 0,
        limit: int = 20
    ):

    # make sure account belongs to current user
    account_query = select(Account).where(
        Account.id == account_id,
        Account.user_id == current_user.id
    )

    result = await db.execute(account_query)

    account = result.scalar_one_or_none()

    if not account:
        raise AccountNotFoundError()

    txn_query = (
        select(Transaction)
        .where(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id)
        )
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(txn_query)

    return result.scalars().all()


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
            raise AccountNotFoundError()

        if acc.user_id != current_user.id:
            raise UnauthorizedAccessError()

        if acc.status == "CLOSED":
            raise AccountAlreadyClosedError()

        if acc.balance != 0:
            raise NonZeroBalanceError()

        acc.status = "CLOSED"

        await db.commit()

        return {"message": "Account closed successfully"}

    except (AccountNotFoundError, UnauthorizedAccessError, AccountAlreadyClosedError, NonZeroBalanceError):
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Account deletion")
