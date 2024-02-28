from redis import asyncio as redis
from fastapi_cache import FastAPICache

from src.settings.config import REDIS_URL, REDIS_URL_FOR_CACHE


async def init_redis():
    global redis_client
    redis_client = redis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    print("Redis client has been initialized")


async def init_redis_cache():
    global redis_client
    redis_client = redis.from_url(REDIS_URL_FOR_CACHE, encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis_client))
    print("Redis cache client has been initialized")
