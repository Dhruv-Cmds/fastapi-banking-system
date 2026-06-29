import redis.asyncio as redis
import os 

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT") or 6379,
    db=os.getenv("REDIS_DB") or 0,
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)
