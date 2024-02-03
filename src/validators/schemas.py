from pydantic import BaseModel, EmailStr, validator, Field
from typing import List


class UserRegister(BaseModel):
    name: str
    lastname: str
    email: EmailStr
    phone_number: str
    username: str
    password: str
    image_bs64: str


class UserLogin(BaseModel):
    username: str
    password: str


class SendEmail(BaseModel):
    email: EmailStr


class CheckCode(BaseModel):
    email: EmailStr
    code: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class VerifyAndNewPassword(BaseModel):
    email: EmailStr
    code: str
    new_password: str


class NewEmployee(BaseModel):
    user_id: int


class UpdatePosition(BaseModel):
    user_id: int
    position: str


class DeleteEmployee(BaseModel):
    user_id: int


class CreateFood(BaseModel):
    name: str
    description: str
    price: float
    type: str
    image_bs64: str


class UpdateFood(BaseModel):
    food_id: int
    name: str
    description: str
    price: float
    type: str
    image_bs64: str


class DeleteFood(BaseModel):
    food_id: int


class AddFavoriteFood(BaseModel):
    food_id: int


class DeleteFavoriteFood(BaseModel):
    food_id: int


class FoodSetCreate(BaseModel):
    name: str
    foods_id: List[int]
    description: str
    price: float
    image_bs64: str


class FoodSetUpdate(BaseModel):
    id: int
    foods_id: List[int]
    name: str
    description: str
    price: float
    image_bs64: str


class FoodSetDelete(BaseModel):
    id: int


class PaymentCreate(BaseModel):
    foods_id: List[int]
    sets_id: List[int]
    place: str


class PaymentUpdate(BaseModel):
    id: int
    foods_id: List[int]
    sets_id: List[int]
    place: str
    is_payed: bool


class PaymentDelete(BaseModel):
    id: int
