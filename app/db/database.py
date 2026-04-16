from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# quote_plus = convert special characters into string.
from urllib.parse import quote_plus


#  Load environment variables
load_dotenv()


# Read DB credentials
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")


# Safety checks (VERY IMPORTANT)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    raise ValueError("Database environment variables are not properly set")


DATABASE_URL = os.getenv("MYSQL_PUBLIC_URL")

# Build database URL
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
# DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


#  Create engine with production-safe settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     #  Avoid stale connections
    pool_size=10,           #  Connection pool size
    max_overflow=20,        #  Extra connections if needed
    echo=False              #  Disable SQL logs in production
)


# Session factory
SessionLocal = sessionmaker(
    bind=engine, 
    autocommit=False, 
    autoflush=False
    )


# Base class for models
Base = declarative_base()


# Dependency for DB session (used in FastAPI routes)
def get_db():

    """
    Provides a database session per request.
    Ensures:
    - connection is opened
    - properly closed after request
    """

    # It Used to read, add, update, delete data.
    db = SessionLocal() 

    try:
        # Give the database connection to who needs it
        yield db
    
    except:  

        # If something goes wrong → rollback
        db.rollback()
        raise
        
    finally:

        # close the database
        db.close() 