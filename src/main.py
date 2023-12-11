from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.dependencies import init_redis, close_redis
from src.routes.auth import auth_router
from src.routes.dish import dish_router
from src.routes.shop import shop_router
from src.routes.queue import queue_router

from src.internal.admin import admin_panel

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на список разрешенных источников
    allow_credentials=True,
    allow_methods=["*"],  # Замените "*" на список разрешенных HTTP-методов
    allow_headers=["*"],  # Замените "*" на список разрешенных HTTP-заголовков
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dish_router, prefix="/dish", tags=["dish"])
app.include_router(shop_router, prefix="/shop", tags=["shop"])
app.include_router(queue_router, prefix="/queue", tags=["queue"])
app.include_router(admin_panel, prefix="/admin", tags=["admin"])


@app.on_event("startup")
async def startup_event():
    init_redis()


@app.on_event("shutdown")
async def shutdown_event():
    close_redis()

