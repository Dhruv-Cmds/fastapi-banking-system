from fastapi import Depends,Header, HTTPException
from jose import jwt, JWTError, ExpiredSignatureError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .db import get_db
from backend.models import User
from backend.core import SECRET_KEY, ALGORITHM

# from fastapi.security import OAuth2PasswordBearer

# Depends(get_db) Opens data Base connection to read, write, delete, update

# takes a token ---> verifies the token, finds the user in data base and return the user  
async def get_current_user(
        authorization: str = Header(None), 
        db: AsyncSession  = Depends(get_db)
    ):


    #  No token provided
    if not authorization:
        raise HTTPException(status_code=401, detail="No token")


    #  Wrong format
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid format")


    # Extract token
    token = authorization.split(" ")[1]


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
