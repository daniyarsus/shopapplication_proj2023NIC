import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import (Base,
                                   async_engine)

from api.services.auth.handlers import auth_router
from api.services.shop.crud.payment.handlers import router as client_payment_router
from api.services.shop.crud.favorite_food.handlers import router as client_favorite_food_router
from api.services.shop.crud.assortment.handlers import router as client_assortment_router

from api.internal.shop.crud.assortment.handlers import shop_router
from api.internal.management.crud.employee.handlers import management_router
from api.internal.auth.crud.user.handlers import router as user_router
from api.internal.shop.crud.payment.handlers import router as payment_router


app = FastAPI(title="FastAPI API",
              description="",
              version="1.0.0",
              docs_url="/api/v1/docs")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""Client API endpoints"""
app.include_router(auth_router,
                   prefix="/api/v1/client/auth",
                   tags=["Client API - auth"])
app.include_router(client_assortment_router,
                   prefix="/api/v1/client/food",
                   tags=["Client API - food"])
app.include_router(client_payment_router,
                   prefix="/api/v1/client/payment",
                   tags=["Client API - payment"])
app.include_router(client_favorite_food_router,
                   prefix="/api/v1/client/favorite_food",
                   tags=["Client API - favorite food"])


"""Admin API endpoints"""
app.include_router(user_router,
                   prefix="/api/v1/user",
                   tags=["Internal API - user"])
app.include_router(shop_router,
                   prefix="/api/v1/food",
                   tags=["Internal API - food"])
app.include_router(management_router,
                   prefix="/api/v1/management",
                   tags=["Internal API - management"])
app.include_router(payment_router,
                   prefix="/api/v1/payment",
                   tags=["Internal API - payment"])


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Server was stopped.")
