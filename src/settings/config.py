import os
#from redis import asyncio as aioredis
import redis
import asyncpg
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.security import OAuth2PasswordBearer


load_dotenv()


#Настройки для SMTP
DOMAIN_NAME = os.getenv("DOMAIN_NAME")
SMTP_PORT = os.getenv("SMTP_PORT")
API_KEY = os.getenv("API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")


#Настройки для базы данных
DATABASE_URL = os.environ.get("DATABASE_URL")
asyncpg_client = asyncpg.connect(DATABASE_URL)
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


#Настройка для токенов
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


#Настройка для Redis
REDIS_URL = os.environ.get("REDIS_URL")
redis_client = redis.from_url(REDIS_URL)
