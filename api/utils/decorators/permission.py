import sqlalchemy.ext.asyncio.base

from api.internal.auth.models import User
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from fastapi.routing import APIRoute
from fastapi import Depends, HTTPException
from functools import wraps


def permission_required(permission_level: int):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args,
                          db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user),
                          **kwargs):
            query = select(User).where(User.id == current_user.id)
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            if user.permission < permission_level:
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(*args, db=db, current_user=current_user, **kwargs)

        return wrapper
    return decorator

