from fastapi import FastAPI
from db.database import engine, Base
from models import user, account
from routes import account, auth



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(account.router)
app.include_router(auth.router)