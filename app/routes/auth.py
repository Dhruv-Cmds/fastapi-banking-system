from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.dependencies import get_current_user
from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserUpdate
from app.core import hash_password, verify_password, create_access_token

router = APIRouter()


# SIGNUP
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    try:
        
        # Case-insensitive username check
        existing = db.query(User).filter(
            func.lower(User.username) == user.username.lower()
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")


        # Hash password before storing
        hashed_pw = hash_password(user.password)

        new_user = User(
            username=user.username.lower(),
            name=user.name,
            password=hashed_pw
        )

        db.begin(

            db.add(new_user),
            db.commit(),
            db.refresh(new_user)
        )

        return {"message": "User created"}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Signup failed")


# LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    try:

        # Case-insensitive lookup
        db_user = db.query(User).filter(
            func.lower(User.username) == user.username.lower()
        ).first()


        # Do NOT reveal whether user exists or password is wrong
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        #  Create JWT token
        token = create_access_token({
            "sub": str(db_user.id)
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Login failed")

#  UPDATE PROFILE
@router.put("/me")
def update_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    try:

        #  Update only allowed fields
        current_user.name = data.name

        db.begin(
            db.commit(),
            db.refresh(current_user)
        )

        return {"message": "Profile updated"}
    
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(500, "Update failed")