from fastapi import Depends, Security
from jose import jwt, JWTError, ExpiredSignatureError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .dbcon import get_db

from app.db.models import User
from app.core import (
    setting,
    UserRole,
    TokenExpiredError,
    InvalidTokenError,
    UserNotFoundError,
    AdminAccessRequiredError
)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Token-based authentication for Swagger and runtime security.
bearer_scheme = HTTPBearer(auto_error=True)

# takes a token ---> verifies the token, finds the user in data base and return the user
async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(bearer_scheme), 
        db: AsyncSession  = Depends(get_db)
    ):

    token = credentials.credentials

    try:
        # verifies token is valid / checks signature using SECRET_KEY / reads hidden data inside
        payload = jwt.decode(
            token, 
            setting.SECRET_KEY, 
            algorithms=[setting.ALGORITHM]
        )

        #  Extract user ID
        sub = payload.get("sub")

        if sub is None:
            raise InvalidTokenError("Invalid token payload")
        
        user_id = int(sub)
        
    except ExpiredSignatureError:
        raise TokenExpiredError()

    except (JWTError, TypeError, ValueError):
        # Invalid / expired / tampered token
        raise InvalidTokenError("Invalid token payload")
    
    # Fetch user from DB
    user_result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )

    user = user_result.scalar_one_or_none()

    if user is None:
        raise UserNotFoundError()
    
    return user


async def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise AdminAccessRequiredError()

    return current_user