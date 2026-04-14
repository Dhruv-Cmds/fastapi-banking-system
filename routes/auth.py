from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from core.security import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    hashed_pw = hash_password(user.password)

    new_user = User(
        username=user.username,
        name=user.name,
        password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    
    ''' we area passing user.passwrod which is plain and db_user.password which are hashed in data base 
        and sending to verify_paaswrod function at core.security to verify is password form database
        and user passed password both are correct or not.'''

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Wrong password")
    
    token = create_access_token({
        "sub": str(db_user.id)   # important
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
