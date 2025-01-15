from fastapi import HTTPException
from redis import asyncio as aioredis
from ..config import settings

redis = aioredis.from_url(settings.REDIS_URL)


async def check_rate_limit(key: str, limit: int, window: int):
    current = await redis.incr(key)
    if current == 1:
        await redis.expire(key, window)

    if current > limit:
        raise HTTPException(
            status_code=429, detail="Too many requests. Please try again later."
        )
