from fastapi import Depends, HTTPException, status, Response
from src.config.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, oauth2_scheme, REDIS_HOST, REDIS_PORT, REDIS_DB
import jwt
from datetime import datetime, timedelta
import redis

from src.database.models import *
from src.config.settings import SessionLocal


# Создание access токена
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Сохранение сессии в Redis
    redis_client.setex(encoded_jwt, int(expires_delta.total_seconds() if expires_delta else 900), str(data['sub']))

    return encoded_jwt


# Получение нужного пользователя
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


# Получение всех пользователей из базы данных
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users


# Открытие Redis
def init_redis():
    global redis_client
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    print("Redis client has been initialized")


# Закрытие Redis
def close_redis():
    global redis_client
    if redis_client:
        redis_client.close()
        print("Redis client has been closed")