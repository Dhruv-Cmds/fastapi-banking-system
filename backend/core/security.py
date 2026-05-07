from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta, timezone

from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
    
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
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add standard JWT fields
    to_encode.update({"exp": expire})  #  user expire time 

    # conver your password into secure string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    ''' SECRET_KEY = lock the data
        ALGORITHM = How data encoded'''
    
    return token