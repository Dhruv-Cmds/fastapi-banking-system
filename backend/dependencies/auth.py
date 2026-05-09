from fastapi import Depends, HTTPException, status, Security
from jose import jwt, JWTError, ExpiredSignatureError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .db import get_db

from backend.models import User
from backend.core import SECRET_KEY, ALGORITHM

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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #  Extract user ID
        user_id = int(payload.get("sub"))

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        # Invalid / expired / tampered token
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Fetch user from DB
    user_result = await db.execute(
        select(User)
        .where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()

    if user is None:

        raise HTTPException(status_code=401, detail="User not found")
    
    return user


async def get_admin_user(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user