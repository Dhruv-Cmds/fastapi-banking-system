from fastapi import FastAPI
from app.db import engine, Base
from app.models import account, user
from app.routes import account, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(account.router)
app.include_router(auth.router)