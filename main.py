from fastapi import FastAPI
from routes import account
import models
from db import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(account.router)