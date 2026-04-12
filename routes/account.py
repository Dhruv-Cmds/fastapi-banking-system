from fastapi import APIRouter, Depends, HTTPException
from models import User, Account
from db.database import SessionLocal
from schemas import AccountCreate, Amount, Transfer, UserCreate
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/accounts")
def create_account(account: AccountCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == account.user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_acc = Account(
        acc_no=account.acc_no,
        balance=account.balance,
        user_id=account.user_id
    )

    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc

@router.get("/accounts")
def get_account(db: Session = Depends(get_db)):
    return db.query(Account).all()

@router.post("/accounts/{id}/deposit")
def deposit(id: int, data: Amount, db: Session = Depends(get_db)):

    acc = db.query(Account).filter(Account.id == id).first()

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    acc.balance += data.amount

    db.commit()
    db.refresh(acc)

    return acc

@router.post("/accounts/{id}/withdraw")
def withdraw(id: int, data: Amount, db: Session = Depends(get_db)):

    acc = db.query(Account).filter(Account.id == id).first()

    if not acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if data.amount > acc.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    acc.balance -= data.amount

    db.commit()
    db.refresh(acc)

    return acc

@router.post("/transfer")
def transfer(data: Transfer, db: Session = Depends(get_db)):

    from_acc = db.query(Account).filter(Account.id == data.from_account_id).first()
    to_acc = db.query(Account).filter(Account.id == data.to_account_id).first()

    if not from_acc or not to_acc:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_acc.id == to_acc.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if from_acc.balance < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    from_acc.balance -= data.amount
    to_acc.balance += data.amount

    db.commit()
    db.refresh(from_acc)
    db.refresh(to_acc)

    return {
        "message": "Transfer successful",
        "from_account_balance": from_acc.balance,
        "to_account_balance": to_acc.balance
    }

@router.post("/test-user")
def test_user(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        name=user.name,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}