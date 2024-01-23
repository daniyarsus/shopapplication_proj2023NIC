import os

import jwt
from fastapi import FastAPI, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from redis import asyncio as aioredis
from datetime import timedelta

from src.auth.signup.register_verification import send_email, verification_code
from src.auth.signup.registration_user import register_user
from src.services.redis_utils.redis_status import init_redis
from src.services.postgres_utils import init_postgres
from src.validators.schemas import *
from src.settings.config import (SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES, REDIS_URL, DATABASE_URL,
                                 SECRET_KEY, REDIS_URL_FOR_CACHE)
from src.database.models import User, FavoriteFood, FoodSet
from src.auth.user.current_user import get_current_user
from src.auth.signin.token import create_access_token
from src.auth.signin.login_user import authenticate_user
from src.auth.password.changing_password import change_user_password
from src.auth.password.password_verification import send_email_forgotten_password, reset_password
from src.auth.user.active_status import activate_user_status, deactivate_user_status
from src.services.redis_utils.redis_users import read_all_redis_data, read_all_redis_data_for_cache
from src.services.redis_utils.cache_key import user_cache_key_builder
from src.shop_development.position_settings import add_employee, delete_employee, update_employee_position
from src.shop_development.products.food_settings import (create_food, update_food, delete_food,
                                                         create_food_set, update_food_set, delete_food_set,
                                                         get_all_assortment, get_all_food_sets)
from src.shop_development.products.favorite_food import add_favorite_food, delete_favorite_food, list_favorite_foods
from src.settings.config import redis_client, redis_client_for_cache
from src.auth.logout.logout_user import logout

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(REDIS_URL_FOR_CACHE,
                              encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis))
    init_redis()
    await init_postgres()


@app.post("/register")
async def register_endpoint(user_in: UserRegister):
    result = await register_user(user_in)
    return result


@app.post("/send-email-for-registration")
async def send_email_endpoint(post_email: SendEmail):
    result = await send_email(post_email)
    return result


@app.post("/verify-email-for-registration")
async def verify_code_endpoint(check: CheckCode):
    result = await verification_code(check)
    return result


@app.post("/token")
async def login_for_access_token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await authenticate_user(form_data)
    return result


@app.delete("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    user_id = str(current_user.id)
    redis_client_for_cache.delete(user_id)
    return {"message": "Logged out successfully and cache cleared"}


@app.put("/change-password")
async def change_password_endpoint(new_password: ChangePassword, current_user: User = Depends(get_current_user)):
    result = await change_user_password(current_user.id, new_password.old_password, new_password.new_password)
    return result


@app.post("/send-email-for-forgotten-password")
async def send_email_forgotten_password_endpoint(email_send: SendEmail):
    result = await send_email_forgotten_password(email_send)
    return result


@app.post("/verify-email-for-forgotten-password")
async def reset_password_endpoint(verify_new_password: VerifyAndNewPassword):
    result = await reset_password(verify_new_password)
    return result


@app.put("/activate-status")
async def activate_user_endpoint(current_user: User = Depends(get_current_user)):
    result = await activate_user_status(current_user)
    return result


@app.put("/deactivate-status")

async def deactivate_user_endpoint(current_user: User = Depends(get_current_user)):
    result = await deactivate_user_status(current_user)
    return result


@app.post("/new-employee")
async def new_employee_endpoint(new_employee: NewEmployee, current_user: User = Depends(get_current_user)):
    result = await add_employee(new_employee, current_user)
    return result


@app.put("/update-position-employee")
async def update_position_employee_endpoint(update_data: UpdatePosition, current_user: User = Depends(get_current_user)):
    result = await update_employee_position(update_data, current_user)
    return result


@app.delete("/delete-employee")
async def delete_employee_endpoint(employee_data: DeleteEmployee, current_user: User = Depends(get_current_user)):
    result = await delete_employee_position(employee_data, current_user)
    return result


@app.post("/create-food")
async def create_food_endpoint(new_food: CreateFood, current_user: User = Depends(get_current_user)):
    result = await create_food(new_food, current_user)
    return result


@app.put("/update-food")
async def update_food_endpoint(food_data: UpdateFood, current_user: User = Depends(get_current_user)):
    result = await update_food(food_data, current_user)
    return result


@app.delete("/delete-food")
async def delete_food_endpoint(del_food: DeleteFood, current_user: User = Depends(get_current_user)):
    result = await delete_food(del_food, current_user)
    return result


@app.get("/get-all-assortment")
@cache(expire=10, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_all_assortment_endpoint(current_user: User = Depends(get_current_user)):
    result = await get_all_assortment(current_user)
    return result


@app.post("/create-set-food")
async def create_set_food_endpoint(food_set: FoodSetCreate, current_user: User = Depends(get_current_user)):
    result = await create_food_set(food_set, current_user)
    return result


@app.put("/update-set-food")
async def update_set_food_endpoint(food_set_data: FoodSetUpdate, current_user: User = Depends(get_current_user)):
    result = await update_food_set(food_set_data, current_user)
    return result


@app.delete("/delete-set-food")
async def update_set_food_endpoint(del_food_set: FoodSetDelete, current_user: User = Depends(get_current_user)):
    result = await delete_food_set(del_food_set, current_user)
    return result


@app.get("/get-all-food-sets")
@cache(expire=10, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_all_food_sets_endpoint(current_user: User = Depends(get_current_user)):
    result = await get_all_food_sets(current_user)
    return result


@app.post("/add-favorite-food")
async def add_favorite_food_endpoint(food_data: AddFavoriteFood, current_user: User = Depends(get_current_user)):
    result = await add_favorite_food(food_data, current_user)
    return result


@app.delete("/delete-favorite-food")
async def delete_favorite_food_endpoint(food_data: DeleteFavoriteFood, current_user: User = Depends(get_current_user)):
    result = await delete_favorite_food(food_data, current_user)
    return result


@app.get("/get-favorite-food")
@cache(expire=10, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_favorite_food_endpoint(current_user: User = Depends(get_current_user)):
    result = await list_favorite_foods(current_user)
    return result


@app.get("/me")
@cache(expire=2, coder=JsonCoder, key_builder=user_cache_key_builder)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "lastname": current_user.lastname,
        "email": current_user.email,
        "username": current_user.username,
        "phone_number": current_user.phone_number,
        "image_url": current_user.image_url,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified
    }


@app.get("/test")
@cache(expire=180)
async def read_users_test(text: str):
    return text


@app.get("/redis-all-information")
async def read_all_redis_data_endpoint():
    result = await read_all_redis_data()
    return result


@app.get("/redis-cache-all-information")
async def read_all_redis_cache_data_endpoint():
    result = await read_all_redis_data_for_cache()
    return result

