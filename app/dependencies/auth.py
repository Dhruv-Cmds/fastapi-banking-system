from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.core import SECRET_KEY, ALGORITHM
from fastapi import Header

# ------------------------------------------------------------------------------------------------

# Depends(get_db) Opens data Base connection to read, write, delete, update

# takes a token ---> verifies the token, finds the user in data base and return the user  
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):

    print("HEADER:", authorization)
    
    if not authorization:
        raise HTTPException(status_code=401, detail="No token")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid format")

    token = authorization.split(" ")[1]


    try:
        # verifies token is valid / checks signature using SECRET_KEY / reads hidden data inside
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = int(payload.get("sub"))

    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(status_code=401, detail="User not found")
    
    return user