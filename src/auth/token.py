import jwt
from datetime import datetime, timedelta

from src.settings.config import SECRET_KEY, ALGORITHM, redis_client


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    redis_client.setex(encoded_jwt, int(expires_delta.total_seconds() if expires_delta else 900), str(data['sub']))
    return encoded_jwt

