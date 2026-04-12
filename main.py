from fastapi import FastAPI
from routes import account
from db.database import engine, Base
from routes import account 
from models import User, Account


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(account.router)