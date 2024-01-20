from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache
import redis
from fastapi import Depends, HTTPException, status

from src.auth.user.current_user import get_current_user
from src.database.models import User


async def logout(current_user: User = Depends(get_current_user)):
#    namespace = user_identifier(current_user)
#    keys = await FastAPICache.backend.get_keys(namespace)
#    if keys:
#        await FastAPICache.backend.delete(*keys)
#    return {"detail": "Cache cleared"}
    pass