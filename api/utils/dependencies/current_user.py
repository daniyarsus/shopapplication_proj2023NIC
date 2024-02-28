from fastapi import HTTPException, Depends

import jwt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.settings.config import settings
from api.services.auth.models import User
from api.services.auth.signin.controllers import oauth2_scheme
from api.utils.dependencies.db import get_db


async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_auth.SECRET_KEY, algorithms=[settings.jwt_auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user
