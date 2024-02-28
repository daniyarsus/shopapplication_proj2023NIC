from datetime import (datetime,
                      timedelta)

from fastapi import (HTTPException,
                     status)
from fastapi.security import (OAuth2PasswordRequestForm,
                              OAuth2PasswordBearer)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from api.services.auth.models import User
from api.settings.config import settings
from api.utils.redis.redis_client import redis_client


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


class SigninManager:
    def __init__(self,
                 form_data: OAuth2PasswordRequestForm,
                 db: AsyncSession):
        self.db = db
        self.form_data = form_data

    async def authenticate_user(self):
        query = select(User).where(User.username == self.form_data.username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Verify code"
            )

        if user.password != self.form_data.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=int(settings.jwt_auth.ACCESS_TOKEN_EXPIRE_MINUTES))
        token_manager = AccessTokenManager(data={"sub": user.username},
                                           expires_delta=access_token_expires)
        access_token = token_manager.create_access_token()
        return {"access_token": access_token, "token_type": "bearer"}


class AccessTokenManager:
    def __init__(self,
                 data: dict,
                 expires_delta: timedelta = None):
        self.data = data
        self.expires_delta = expires_delta or None
        self.to_encode = self.data.copy()

    def create_access_token(self):
        if self.expires_delta:
            expire = datetime.utcnow() + self.expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        self.to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(self.to_encode,
                                 settings.jwt_auth.SECRET_KEY,
                                 algorithm=settings.jwt_auth.ALGORITHM
                                 )

        redis_client.setex(encoded_jwt,
                           int(self.expires_delta.total_seconds() if self.expires_delta else 900),
                           str(self.data['sub'])
                           )

        return encoded_jwt


#class RefreshTokenManager:
#    def __init__(self, user: User, expires_delta: timedelta = None):
#        self.user = user
#        self.expires_delta = expires_delta or None
#
#    def create_refresh_token(self):
#        data = {"sub": self.user.username, "type": "refresh"}
#        if self.expires_delta:
#            expire = datetime.utcnow() + self.expires_delta
#        else:
#            expire = datetime.utcnow() + timedelta(days=30)  # Refresh token valid for 30 days
#        data.update({"exp": expire})
#        encoded_jwt = jwt.encode(data, settings.jwt_auth.SECRET_KEY, algorithm=settings.jwt_auth.ALGORITHM)
#        redis_client.setex(encoded_jwt, int(self.expires_delta.total_seconds() if self.expires_delta else 2592000), str(data['sub']))
#        return encoded_jwt
#
#    @staticmethod
#    async def refresh(refresh_token: str):
#        try:
#            payload = jwt.decode(refresh_token, settings.jwt_auth.SECRET_KEY, algorithms=[settings.jwt_auth.ALGORITHM])
#            username: str = payload.get("sub")
#            if username is None or payload.get("type") != "refresh":
#                raise credentials_exception
#            token_expired = int(redis_client.ttl(refresh_token))
#            if token_expired == -2:
#                raise credentials_exception
#            new_access_token = AccessTokenManager.create_access_token(data={"sub": username})
#            return {"access_token": new_access_token, "token_type": "bearer"}
#        except JWTError:
#            raise credentials_exception

