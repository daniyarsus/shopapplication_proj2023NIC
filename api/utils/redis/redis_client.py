import redis

from api.settings.config import settings


redis_client = redis.from_url(settings.redis_user.REDIS_USER_DATABASE_URL)

