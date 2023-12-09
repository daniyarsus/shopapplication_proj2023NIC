from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.dependencies import init_redis, close_redis
from routes.auth import auth_router
from routes.dish import dish_router
from routes.shop import shop_router
from routes.queue import queue_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на список разрешенных источников
    allow_credentials=True,
    allow_methods=["*"],  # Замените "*" на список разрешенных HTTP-методов
    allow_headers=["*"],  # Замените "*" на список разрешенных HTTP-заголовков
)

app.include_router(auth_router)
app.include_router(dish_router, prefix="/dish", tags=["dish"])
app.include_router(shop_router, prefix="/shop", tags=["shop"])
app.include_router(queue_router, prefix="/queue", tags=["queue"])


@app.on_event("startup")
async def startup_event():
    init_redis()


@app.on_event("shutdown")
async def shutdown_event():
    close_redis()