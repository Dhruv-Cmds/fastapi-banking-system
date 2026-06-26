from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


from app.db.models import User

from app.schemas import UserCreate, UserUpdate

from app.core import (
    logger,
    hash_password, 
    UsernameAlreadyExistsError,
    DatabaseError
)


async def create_user(db: AsyncSession, user: UserCreate):

    try:

        new_user = User(
            username=user.username.lower(),
            name=user.name,
            password=hash_password(user.password)
        )

        db.add(new_user)
        await db.commit()
        await db.flush()

        logger.info(
            "User created successfully (user_id=%s)",
            new_user.id
        )

        return new_user
    
    except IntegrityError:

        await db.rollback()

        logger.exception(
            "Database integrity error while creating user"
        )

        raise UsernameAlreadyExistsError()

    
async def update_profile(
        db: AsyncSession, 
        data: UserUpdate, 
        current_user:User
    ):
    
    try:

        if data.name:
            current_user.name = data.name

        if data.password:
            current_user.password = hash_password(data.password)

        db.add(current_user)

        await db.commit()

        return current_user

    except SQLAlchemyError:

        await db.rollback()

        raise DatabaseError()