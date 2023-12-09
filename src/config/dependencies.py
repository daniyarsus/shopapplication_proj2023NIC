from fastapi import Depends, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
import redis
from schemas.validators import *
from database.models import *


# Security and authentication
SECRET_KEY = "12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Настройки Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# Подключение к Redis
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


# Helper functions
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




# Функция для получения всех пользователей из базы данных
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users




import redis

# Настройки Redis
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


def init_redis():
    global redis_client
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    print("Redis client has been initialized")


def close_redis():
    global redis_client
    if redis_client:
        redis_client.close()
        print("Redis client has been closed")