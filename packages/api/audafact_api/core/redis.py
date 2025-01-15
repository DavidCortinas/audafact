from redis import asyncio as aioredis
from ..config import settings

redis = aioredis.from_url(settings.REDIS_URL)


async def store_verification_code(email: str, code: str):
    # Store code with 10-minute expiration
    await redis.set(f"verification_code:{email}", code, ex=600)


async def get_verification_code(email: str):
    return await redis.get(f"verification_code:{email}")


async def delete_verification_code(email: str):
    await redis.delete(f"verification_code:{email}")
