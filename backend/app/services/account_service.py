from sqlalchemy import or_, select, and_

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.db.models import Account, Transaction, User

from app.schemas import AccountCreate,Transfer, Amount

from app.core import (

    MAX_DEPOSIT, 
    MAX_WITHDRAW, 
    MAX_TRANSFER,

    logger,

    UserRole,
    UserStatus,
    AccountStatus,
    PaymentStatus,

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
    PermissionDeniedError,
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

    if account.status != UserStatus.ACTIVE:
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

        logger.info(
            "Account created successfully by (user_id=%s)",
            current_user.id
        )

        return new_acc

    except IntegrityError:
        await db.rollback()
        raise AccountAlreadyExistsError()

    except SQLAlchemyError:
        await db.rollback()
        raise DatabaseError("Account creation")


async def get_accounts(db: AsyncSession, current_user):

    result = await db.execute(
        select(Account)
        .where(Account.user_id == current_user.id)
    )
    
    return result.scalars().all()


async def deposit(db: AsyncSession, id, data: Amount, current_user):

    try:

        if data.amount > MAX_DEPOSIT:

            logger.warning(
                "Amount limit exicuted: cannot DEPOSIT money more %s",
                MAX_DEPOSIT
            )

            raise DepositLimitExceededError()

        account = await _get_owned_account_for_update(db, id, current_user)
        account.balance += data.amount

        db.add(Transaction(
            from_account_id=None,
            to_account_id=id,
            amount=data.amount,
            status=PaymentStatus.SUCCESS
        ))

        await db.commit()

        logger.warning(
            "Amount=%s deposit successfully",
            data.amount,
        )

        return account

    except (
        DepositLimitExceededError, 
        AccountNotFoundError, 
        AccountInactiveError
    ):
        await db.rollback()
        raise

    except SQLAlchemyError:
        
        await db.rollback()
        raise DatabaseError()


# WITHDRAW
async def withdraw(db: AsyncSession, id, data: Amount, current_user):

    try:

        if data.amount > MAX_WITHDRAW:

            logger.warning(
                "Amount limit exicuted: cannot WITHDRAW money more %s",
                MAX_WITHDRAW
            )

            raise WithdrawLimitExceededError()

        account = await _get_owned_account_for_update(db, id, current_user)

        if account.balance < data.amount:

            logger.warning(
                "Insufficient balance: Withdraw amount=%s is grater then current balance=%s",
                data.amount,
                account.balance
            )

            raise InsufficientFundsError()

        account.balance -= data.amount

        db.add(Transaction
            (
                from_account_id=id,
                to_account_id=None,
                amount=data.amount,
                status=PaymentStatus.SUCCESS
        )   )  

        await db.commit()

        logger.info(
            "(Amount=%s) withdraw successfully by (user_id=%s)",
            data.amount,
            account.user_id
        )
        return account

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
async def transfer(db: AsyncSession, data:Transfer, current_user):

    try:

        if data.amount > MAX_TRANSFER:

            logger.warning(
                "Transfer amount limit exicuted: cannot transfer money more then %s",
                MAX_TRANSFER
            )

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

            logger.warning(
                "Account not found (from_acc=%s) , (to_acc=%s)",
                from_acc,
                to_acc
            )
            raise AccountNotFoundError()

        if from_acc.status != AccountStatus.ACTIVE:

            logger.warning(
                "User account is not active (user_acc=%s) , (status=%s)",
                from_acc,
                from_acc.status
            )
            raise AccountInactiveError()

        if to_acc.status != AccountStatus.ACTIVE:

            logger.warning(
                "User account is not active (user_acc=%s) , (status=%s)",
                to_acc,
                to_acc.status
            )
            raise AccountInactiveError()

        if from_acc.id == to_acc.id:

            logger.warning(
                "Transaction failed: cannot send to your own account"
                "from_acc=%s , to_acc=%s",
                from_acc,
                to_acc
            )
            raise UnauthorizedAccessError()

        if from_acc.balance < data.amount:

            logger.warning(
                "Insufficient balance: transfer amount=%s is grater then current balance=%s",
                data.amount,
                from_acc.balance
            )
            raise InsufficientFundsError()

        from_acc.balance -= data.amount
        to_acc.balance += data.amount

        db.add(Transaction(
            from_account_id=from_acc.id,
            to_account_id=to_acc.id,
            amount=data.amount,
            status=PaymentStatus.SUCCESS
        ))

        logger.info(
            "Transfer successfullt from_acc=%s to to_acc=%s",
            from_acc,
            to_acc
        )

        await db.commit()

        return (
            from_acc.id,
            to_acc.acc_no,
            data.amount
        )

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
        raise DatabaseError()
    
async def get_transactions(
        db: AsyncSession,
        account_id: int,
        current_user: User,
        skip: int = 0,
        limit: int = 20
    ):

    # make sure account belongs to current user
    account_query = await db.execute(
        select(Account)
        .where(
            and_(
                (Account.id == account_id),
                (Account.user_id == current_user.id)
            )
        )
    )

    account = account_query.scalar_one_or_none()

    if not account:

        logger.warning(
            "Account not found for transactions (account_id=%s), (user_id=%s)",
            account.id,
            current_user.id
        )
        raise AccountNotFoundError()

    txn_query = await db.execute(
        select(Transaction)
        .where(
            or_(
                (Transaction.from_account_id == account_id),
                (Transaction.to_account_id == account_id)
            )
        )
        .order_by(Transaction.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return txn_query.scalars().all()


# DELETE ACCOUNT
async def delete_account(
    db: AsyncSession,
    current_user: User,
    account_id: int,
):
    try:
        result = await db.execute(
            select(Account)
            .where(Account.id == account_id)
            .with_for_update()
        )
        acc = result.scalar_one_or_none()

        if not acc:

            logger.info(
                "Account not found (account_id=%s)", 
                account_id
            )
            raise AccountNotFoundError()

        # Check ownership AFTER loading the account
        if (
            current_user.role != UserRole.ADMIN 
            and acc.user_id != current_user.id
        ):
            logger.warning(
                "Account close failed: user %s is not allowed to close account %s",
                current_user.id,
                account_id,
            )
            raise PermissionDeniedError()

        if acc.status == AccountStatus.CLOSED:

            logger.warning(
                "Account already closed (account_id=%s)", 
                account_id
            )
            raise AccountAlreadyClosedError()

        if acc.balance != 0:

            logger.warning(
                "Account close failed: account_id=%s has non-zero balance (%s)",
                account_id,
                acc.balance,
            )
            raise NonZeroBalanceError()

        acc.status = AccountStatus.CLOSED
        await db.commit()
        await db.refresh(acc)

        logger.info(
            "Account Close successfully (acc_id=%s)",
            acc.id
        )
        return acc

    except (
        AccountNotFoundError,
        PermissionDeniedError,
        AccountAlreadyClosedError,
        NonZeroBalanceError,
    ):
        await db.rollback()
        raise

    except SQLAlchemyError:
        await db.rollback()
        logger.exception("Database error while closing account_id=%s", account_id)
        raise DatabaseError("Account deletion")
