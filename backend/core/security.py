from fastapi import HTTPException

from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta
from dotenv import load_dotenv

import os

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


# Safety check (VERY IMPORTANT)
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set in environment variable")

    
#  Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hashed password
def hash_password(password: str):
    return pwd_context.hash(password)


# verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


# create access token (JWT)
def create_access_token(data: dict): # user info come in json (dict) formate

    #  made copy so original data will stay safe
    to_encode = data.copy()

    #  decide when to expire user token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add standard JWT fields
    to_encode.update({"exp": expire})  #  user expire time 

    # conver your password into secure string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    ''' SECRET_KEY = lock the data
        ALGORITHM = How data encoded'''
    
    return token