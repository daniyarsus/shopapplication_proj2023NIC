from fastapi import HTTPException, Request
from api.services.auth.models import User
from api.utils.dependencies.current_user import get_current_user
from typing import Callable
import functools
from typing import Callable
from fastapi.routing import APIRoute


def permission_required(permission: int) -> Callable[[APIRoute], APIRoute]:
    def decorator(route: APIRoute) -> APIRoute:
        async def wrapper(*args, **kwargs) -> None:
            user = await get_current_user()
            if user.permission != permission:
                raise HTTPException(status_code=403, detail="Permission denied")
            return await route(*args, **kwargs)
        return wrapper
    return decorator
