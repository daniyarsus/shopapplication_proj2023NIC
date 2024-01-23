import redis

from src.settings.config import REDIS_URL, REDIS_URL_FOR_CACHE


async def read_all_redis_data():
    try:
        client = redis.from_url(REDIS_URL)
        keys = client.keys('*')
        data = {}
        for key in keys:
            value = client.get(key)
            if value is not None:
                data[key.decode('utf-8')] = value.decode('utf-8')
        return data
    except Exception as e:
        return {"error": f"Failed to connect to Redis: {e}"}


async def read_all_redis_data_for_cache():
    try:
        client = redis.from_url(REDIS_URL_FOR_CACHE)
        keys = client.keys('*')
        data = {}
        for key in keys:
            value = client.get(key)
            if value is not None:
                data[key.decode('utf-8')] = value.decode('utf-8')
        return data
    except Exception as e:
        return {"error": f"Failed to connect to Redis: {e}"}

