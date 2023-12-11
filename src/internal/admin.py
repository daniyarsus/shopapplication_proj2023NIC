from fastapi import APIRouter
import redis

from src.config.settings import REDIS_URL
from src.config.dependencies import get_all_users, get_all_shops

admin_panel = APIRouter()


@admin_panel.get("/redis/all")
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


# Эндпоинт для вывода всех данных из таблицы Users
@admin_panel.get("/users_all")
async def read_all_users():
    users = get_all_users()
    return users


@admin_panel.get("/shops_all")
async def read_all_shops():
    shops = get_all_shops()
    return shops