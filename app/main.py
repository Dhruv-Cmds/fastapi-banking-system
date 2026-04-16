from fastapi import FastAPI
from app.db import engine, Base

from app.models import account, user
from app.routes import account, auth
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI()

origins = [
    "http://localhost:5173",     # frontend
    "http://127.0.0.1:5173"      # backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create DB tables (for development only)
Base.metadata.create_all(bind=engine)


# Register routes with prefixes (clean API structure)
app.include_router(account.router)
app.include_router(auth.router)