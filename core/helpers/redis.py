import redis.asyncio as aioredis

from core.config import config

redis = aioredis.from_url(url=f"redis://{config.REDIS_HOST}")


def generate_redis():
    return aioredis.from_url(url=f"redis://{config.REDIS_HOST}")
