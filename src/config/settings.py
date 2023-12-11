from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import redis

from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from dotenv import load_dotenv
import os

load_dotenv()


# Настройки Redis
#REDIS_PASSWORD = ""
REDIS_URL = f"redis://default:eb3ALfHIf6IGn5HmFBpB33aoPNbAfhlm@roundhouse.proxy.rlwy.net:21053"
redis_client = redis.from_url(REDIS_URL)


# Настройка JWT
SECRET_KEY = "Iloveuourmom"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# Настройка SQLAlchemy DB
DATABASE_URL = "postgresql://postgres:4ddE6a*d**CcDB6aebd-42FeCb1EdFCb@monorail.proxy.rlwy.net:22344/railway"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


