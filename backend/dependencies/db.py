from backend.db import AsyncSessionLocal

# Dependency for DB session (used in FastAPI routes)
async def get_db():

    # It Used to read, add, update, delete data.
    async with AsyncSessionLocal() as db:
        # Give the database connection to who needs it
        yield db