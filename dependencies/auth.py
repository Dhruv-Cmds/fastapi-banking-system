from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from core.security import SECRET_KEY, ALGORITHM

# ------------------------------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

''' OAuth2PasswordBearer = ''' # FastApi automatically looks for token 
''' Authorization: Bearer <your_token>'''

'''Example: ''' # token = "eyJhbGciOiJIUzI1NiIs..." 

''' db:Session = Depends(get_db) = ''' # Opens data Base connection to read, write, delete, update

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    '''token = ''' # takes a token ---> verifies the token
    ''' db:Session = ''' # finds the user in data base and return the user  

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        '''payload = ''' # verifies token is valid / checks signature using SECRET_KEY / reads hidden data inside

        user_id = int(payload.get("sub"))

    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check does this user actually exist or not
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:

        raise HTTPException(status_code=401, detail="User not found")
    
    return user