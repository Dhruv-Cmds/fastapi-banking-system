import redis.asyncio as redis
import os 
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT") or 6379,
    db=os.getenv("REDIS_DB") or 0,
    decode_responses=True
)
