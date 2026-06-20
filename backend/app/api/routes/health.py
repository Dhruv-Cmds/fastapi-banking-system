from fastapi import APIRouter
from sqlalchemy import text
from app.db import engine

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment checks.
    Returns app status and checks database connectivity.
    """
    try:
        # Check database connectivity
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        return {
            "status": "healthy",
            "database": "connected",
            "message": "Application is running and database is accessible"
        }
    
    except Exception:
        
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "message": "Application is running but database is not accessible"
        }