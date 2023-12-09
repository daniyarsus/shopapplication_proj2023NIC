from pydantic import BaseModel


# Pydantic models
class UserIn(BaseModel):
    username: str
    password: str


class Logout(BaseModel):
    access_token: str


class ShopCreate(BaseModel):
    name: str


class DishCreate(BaseModel):
    name: str
    shop_id: int


class QueueAdd(BaseModel):
    dish_id: int
    shop_id: int


class QueueReady(BaseModel):
    shop_id: int
    queue_id: int


class ShopMenuRequest(BaseModel):
    shop_id: int


# Pydantic model для обновления пароля
class UpdatePassword(BaseModel):
    old_password: str
    new_password: str