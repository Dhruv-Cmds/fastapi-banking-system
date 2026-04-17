from fastapi import Depends, HTTPException
from jose import jwt, JWSError
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.core import SECRET_KEY, ALGORITHM
from fastapi import Header
# from fastapi.security import OAuth2PasswordBearer



# Depends(get_db) Opens data Base connection to read, write, delete, update

# takes a token ---> verifies the token, finds the user in data base and return the user  
def get_current_user(
        authorization: str = Header(None), 
        db: Session = Depends(get_db)
    ):

    """
    Extracts and verifies JWT token
    Returns authenticated user
    """
    

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

    except JWSError:

        # Invalid / expired / tampered token
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Fetch user from DB
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     """
#     Extracts and verifies JWT token
#     Returns authenticated user
#     """

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#         user_id = int(payload.get("sub"))

#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")

#     except JWSError:
#         raise HTTPException(status_code=401, detail="Invalid token")

#     user = db.query(User).filter(User.id == user_id).first()

#     if user is None:
#         raise HTTPException(status_code=401, detail="User not found")

#     return user