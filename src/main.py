from fastapi import FastAPI, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.settings.config import REDIS_URL_FOR_CACHE
from src.services.redis_utils.redis_status import init_redis
from src.services.postgres_utils import init_postgres
from src.routers import api_router


app = FastAPI(
    title="DoughJoy Delights API",
    description="API for DoughJoy Delights",
    contact={"name": "Hui",
             "email": "daniyar.kanu@gmail.com",
             "x-telegram": "danyaKex"},
    version="1.0.0",
    docs_url="/api/v1/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1", tags=["DoughJoy Delights API v1"])


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(REDIS_URL_FOR_CACHE,
                              encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis))
    init_redis()
    await init_postgres()

