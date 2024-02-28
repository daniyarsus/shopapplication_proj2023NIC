from redis import asyncio as redis
from fastapi import HTTPException, status

from src.settings.config import REDIS_URL, REDIS_URL_FOR_CACHE
from src.database.models import Employee


class ReadRedisData:
    def __init__(self, current_user, db):
        self.current_user = current_user
        self.db = db

    async def _check_owner(self):
        employee = self.db.query(Employee).filter(
            Employee.user_id == self.current_user.id,
            Employee.position.lower() == "owner"
        ).first()
        if not employee:
            raise HTTPException(status_code=403, detail="You are not authorized to perform this operation")

    async def read_users_in_redis(self):
        await self._check_owner()

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

    async def read_cache_in_redis(self):
        await self._check_owner()

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

