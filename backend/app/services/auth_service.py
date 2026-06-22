from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.schemas import UserCreate
from app.services import user_service

from app.core import(
    logger,
    verify_password, 
    create_access_token,
    InvalidCredentialsError,
)


async def signup(
        db: AsyncSession ,
        user: UserCreate,
    ):

    return await user_service.create_user(db, user)


async def login(
        db:AsyncSession,
        username: str,
        password: str 
    ):
        result = await db.execute(
            select(User)
            .where(func.lower(User.username) == username.lower())
        )

        user = result.scalar_one_or_none()

        if user is None:

            logger.warning(
                "Login failed: user not found for username '%s'",
                username
            )

        if not verify_password(password, user.password):

            logger.warning(
                "Login failed: invalid password for user ID %s",
                user.id
            )

            raise InvalidCredentialsError()

        token = create_access_token(
            {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }