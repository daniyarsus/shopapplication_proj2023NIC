import os

from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class PostgresDataBaseSettings:
    POSTGRES_DATABASE_URL = os.environ.get("POSTGRES_DATABASE_URL")


@dataclass
class RegisUserDataBaseSettings:
    REDIS_USER_DATABASE_URL = os.environ.get("REDIS_USER_DATABASE_URL")


@dataclass
class RedisCacheDataBaseSettings:
    REDIS_CACHE_DATABASE_URL = os.environ.get("REDIS_CACHE_DATABASE_URL")


@dataclass
class SMTPSettings:
    DOMAIN_NAME = os.environ.get("DOMAIN_NAME")
    SMTP_PORT = os.environ.get("SMTP_PORT")
    API_KEY = os.environ.get("API_KEY")
    EMAIL_FROM = os.environ.get("EMAIL_FROM")


@dataclass
class JWTSettings:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")


@dataclass
class Settings:
    def __init__(self):
        self.pg_database = PostgresDataBaseSettings()
        self.redis_user = RegisUserDataBaseSettings()
        self.redis_cache = RedisCacheDataBaseSettings()
        self.smtp_gmail = SMTPSettings()
        self.jwt_auth = JWTSettings()


settings: Settings = Settings()
