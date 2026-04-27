from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import engine, Base

from backend.routes import auth as auth_routes
from backend.routes import account as account_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# include routers properly
app.include_router(auth_routes.router, prefix="/api")
app.include_router(account_routes.router, prefix="/api")
