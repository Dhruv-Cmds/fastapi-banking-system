from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# user info come in json (dict) formate
def create_access_token(data: dict):

    #  made copy so original data will stay safe
    to_encode = data.copy()

    #  decide when to expire user token
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    #  this gives you user expire time 
    to_encode.update({"exp": expire})

    # this conver your password into secure string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    ''' SECRET_KEY = lock the data
        ALGORITHM = How data encoded'''
    
    return token