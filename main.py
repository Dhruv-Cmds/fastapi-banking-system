from fastapi import FastAPI
from routes import account
from db.database import engine, Base
from models import User, Account
from routes import account, auth



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(account.router)
app.include_router(auth.router)