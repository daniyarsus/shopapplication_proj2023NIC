import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import (Base,
                                   async_engine)

from api.services.auth.handlers import auth_router
from api.internal.shop.handlers import shop_router
from api.internal.management.handlers import management_router


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


app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth API"])
app.include_router(shop_router, prefix="/api/v1/internal/shop", tags=["Internal API - shop"])
app.include_router(management_router, prefix="/api/v1/internal/management", tags=["Internal API - management"])


@app.on_event("startup")
async def startup() -> None:
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except asyncio.exceptions.CancelledError:
        print("Server was stopped.")


@app.get("/")
async def index():
    return {"message": "Hello world"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port="8000")

