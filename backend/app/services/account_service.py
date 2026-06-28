from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.db.models import Account, Transaction, User
from app.schemas import AccountCreate,Transfer
from app.repository import account_repository
from app.core import (

    MAX_DEPOSIT, 
    MAX_WITHDRAW, 
    MAX_TRANSFER,

    logger,

    UserRole,
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
        raise DatabaseError()


async def get_accounts(db: AsyncSession, current_user: User):
    return await account_repository.get_accounts_by_user_id(db, current_user.id)
    

async def deposit(
        db: AsyncSession, 
        account_id, 
        amount, 
        current_user: User
    ):

    try:

        if amount > MAX_DEPOSIT:

            logger.warning(
                "Amount limit exicuted: cannot DEPOSIT money more %s",
                MAX_DEPOSIT
            )

            raise DepositLimitExceededError()

        account = await account_repository.get_owned_account(
            db, 
            account_id, 
            current_user
        )

        if not account:

            logger.warning(
                "Deposite failed: account not found (account_id=%s), (user_id=%s)",
                account_id,
                current_user.id
            )
            raise AccountNotFoundError()

        if account.status != AccountStatus.ACTIVE:

            logger.warning(
                "Deposite failed: user status is not active (account_id=%s), (user_id=%s), (account_status=%s)",
                account_id,
                current_user.id,
                account.status
            )
            raise AccountInactiveError()


        account.balance += amount

        db.add(Transaction(
            from_account_id=None,
            to_account_id=account_id,
            amount=amount,
            status=PaymentStatus.SUCCESS
        ))

        await db.flush()
        await db.commit()

        logger.warning(
            "Amount=%s deposit successfully",
            amount,
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
async def withdraw(
        db: AsyncSession, 
        account_id, 
        amount, 
        current_user: User
    ):

    try:

        if amount > MAX_WITHDRAW:

            logger.warning(
                "Amount limit exicuted: cannot WITHDRAW money more %s",
                MAX_WITHDRAW
            )

            raise WithdrawLimitExceededError()

        account = await account_repository.get_owned_account(
            db, 
            account_id, 
            current_user
        )

        if not account:

            logger.warning(
                "Withdraw failed: account not found (account_id=%s), (user_id=%s)",
                account_id,
                current_user.id
            )
            raise AccountNotFoundError()

        if account.status != AccountStatus.ACTIVE:

            logger.warning(
                "Withdraw failed: user status is not active (account_id=%s), (user_id=%s), (account_status=%s)",
                account_id,
                current_user.id,
                account.status
            )
            raise AccountInactiveError()
        
        if account.balance < amount:

            logger.warning(
                "Insufficient balance: Withdraw amount=%s is grater then current balance=%s",
                amount,
                account.balance
            )
            raise InsufficientFundsError()

        account.balance -= amount

        db.add(Transaction
            (
                from_account_id=account_id,
                to_account_id=None,
                amount=amount,
                status=PaymentStatus.SUCCESS
        )   )  

        await db.commit()
        await db.refresh(account)

        logger.info(
            "(Amount=%s) withdraw successfully by (user_id=%s)",
            amount,
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
        raise DatabaseError()


# TRANSFER
async def transfer(
        db: AsyncSession, 
        data:Transfer, 
        current_user: User
    ):

    try:

        if data.amount > MAX_TRANSFER:

            logger.warning(
                "Transfer amount limit exicuted: cannot transfer money more then %s",
                MAX_TRANSFER
            )
            raise TransferLimitExceededError()


        accounts = await account_repository.get_accounts_for_transfer(db, data)

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

        return {
            "from_account_id": from_acc.id,
            "to_account_no": to_acc.acc_no,
            "amount": data.amount,
            "message": "Transfer successful"
        }

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

    account = await account_repository.get_owned_account(
        db,
        account_id,
        current_user
    )

    if not account:

        logger.warning(
            "Withdraw failed: account not found (account_id=%s), (user_id=%s)",
            account_id,
            current_user.id
        )
        raise AccountNotFoundError()
    
    return await account_repository.get_transactions(
        db,
        account_id,
        skip=skip,
        limit=limit
    )


# DELETE ACCOUNT
async def delete_account(
        db: AsyncSession,
        current_user: User,
        account_id: int,
    ):

    try:

        account = await account_repository.get_account(
            db,
            account_id,
        )

        if not account:

            logger.info(
                "Account not found (account_id=%s)", 
                account_id,
            )
            raise AccountNotFoundError()

        # Check ownership AFTER loading the account
        if (
            current_user.role != UserRole.ADMIN 
            and account.user_id != current_user.id
        ):
            logger.warning(
                "Account close failed: user %s is not allowed to close account %s",
                current_user.id,
                account_id,
            )
            raise PermissionDeniedError()

        if account.status == AccountStatus.CLOSED:

            logger.warning(
                "Account already closed (account_id=%s)", 
                account_id
            )
            raise AccountAlreadyClosedError()

        if account.balance != 0:

            logger.warning(
                "Account close failed: account_id=%s has non-zero balance (%s)",
                account_id,
                account.balance,
            )
            raise NonZeroBalanceError()

        account.status = AccountStatus.CLOSED

        await db.commit()
        await db.refresh(account)

        logger.info(
            "Account Close successfully (acc_id=%s)",
            account.id
        )

        return account
    
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
        raise DatabaseError()
