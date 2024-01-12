import redis

from src.settings.config import REDIS_URL


async def read_all_redis_data():
    try:
        client = redis.from_url("redis://default:h2CfIgbLenME656D5F1e2K6Bd2He1B3a@viaduct.proxy.rlwy.net:28951")
        keys = client.keys('*')
        data = {}
        for key in keys:
            value = client.get(key)
            if value is not None:
                data[key.decode('utf-8')] = value.decode('utf-8')
        return data
    except Exception as e:
        return {"error": f"Failed to connect to Redis: {e}"}

