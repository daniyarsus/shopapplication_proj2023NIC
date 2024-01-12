import redis

from src.settings.config import REDIS_URL


def init_redis():
    global redis_client
    redis_client = redis.from_url(REDIS_URL)
    print("Redis client has been initialized")


