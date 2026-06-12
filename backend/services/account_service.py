from sqlalchemy import or_, select

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from backend.models import Account, Transaction, User

from backend.schemas import AccountCreate
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


async def _get_owned_account_for_update(db: AsyncSession, account_id: int, current_user: User):
    result = await db.execute(
        select(Account)
        .where(
            Account.id == account_id,
            Account.user_id == current_user.id
        )
        .with_for_update()
    )

    account = result.scalar_one_or_none()

    if not account:
        raise AccountNotFoundError()

    if account.status != "ACTIVE":
        raise AccountInactiveError()

    return account


# CREATE
async def create_account(
        db: AsyncSession, 
        account: AccountCreate, 
        current_user:User 
    ):

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

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Account creation")


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

        account = await _get_owned_account_for_update(db, id, current_user)
        account.balance += data.amount

        db.add(Transaction(
            from_account_id=None,
            to_account_id=id,
            amount=data.amount,
            status="SUCCESS"
        ))

        await db.commit()

        return {"message": "Deposit successful"}

    except (DepositLimitExceededError, AccountNotFoundError, AccountInactiveError):
        await db.rollback()
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Deposit operation")


# WITHDRAW
async def withdraw(db: AsyncSession, id, data, current_user):

    try:

        if data.amount > MAX_WITHDRAW:
            raise WithdrawLimitExceededError()

        account = await _get_owned_account_for_update(db, id, current_user)

        if account.balance < data.amount:
            raise InsufficientFundsError()

        account.balance -= data.amount

        db.add(Transaction(
            from_account_id=id,
            to_account_id=None,
            amount=data.amount,
            status="SUCCESS"
        ))

        await db.commit()

        return {"message": "Withdraw successful"}

    except (
        WithdrawLimitExceededError,
        AccountNotFoundError,
        AccountInactiveError,
        InsufficientFundsError
    ):
        await db.rollback()
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Withdrawal operation")


# TRANSFER
async def transfer(db: AsyncSession, data, current_user):

    try:

        if data.amount > MAX_TRANSFER:
            raise TransferLimitExceededError()

        result = await db.execute(
            select(Account)
            .where(
                or_(
                    Account.id == data.from_account_id,
                    Account.acc_no == data.to_account_no
                )
            )
            .order_by(Account.id)
            .with_for_update()
        )
        accounts = result.scalars().all()

        from_acc = next(
            (
                account for account in accounts
                if (
                    account.id == data.from_account_id and
                    account.user_id == current_user.id
                )
            ),
            None
        )
        to_acc = next(
            (
                account for account in accounts
                if account.acc_no == data.to_account_no
            ),
            None
        )

        if not from_acc or not to_acc:
            raise AccountNotFoundError()

        if from_acc.status != "ACTIVE":
            raise AccountInactiveError()

        if to_acc.status != "ACTIVE":
            raise AccountInactiveError()

        if from_acc.id == to_acc.id:
            raise UnauthorizedAccessError("Cannot transfer to the same account")

        if from_acc.balance < data.amount:
            raise InsufficientFundsError()

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

    except (
        TransferLimitExceededError,
        AccountNotFoundError,
        AccountInactiveError,
        UnauthorizedAccessError,
        InsufficientFundsError
    ):
        await db.rollback()
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
        await db.rollback()
        raise

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Account deletion")
