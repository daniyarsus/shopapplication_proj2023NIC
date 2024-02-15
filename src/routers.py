from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder

from src.auth.signup.register_verification import send_email, verification_code
from src.validators.schemas import *
from src.database.models import User
from src.auth.signin.login_user import authenticate_user
from src.auth.password.password_verification import send_email_forgotten_password, reset_password
from src.services.redis_utils.redis_users import read_all_redis_data, read_all_redis_data_for_cache
from src.services.redis_utils.cache_key import user_cache_key_builder
from src.shop.products.favorite_food import add_favorite_food, delete_favorite_food, list_favorite_foods
from src.settings.config import redis_client_for_cache
from src.shop.payment.payment_settings import create_payment, update_payment, delete_payment
from src.auth.user.info_about_user import info_about_me


from src.dependencies.current_user import get_current_user
from src.dependencies.db import get_db


from src.auth.signup.registration_user import RegistrationUser
from src.auth.password.changing_password import ChangingPassword
from src.auth.user.active_status import UserActivateStatus, UserDeactivateStatus
from src.shop.employee.position_settings import EmployeeManager
from src.shop.products.base_food import FoodManager
from src.shop.products.food_set import FoodSetManager

api_router = APIRouter()


@api_router.post("/registration")
async def register_endpoint(user_in: UserRegister,
                            db: Session = Depends(get_db)):
    registration_user = RegistrationUser(user_in, db)
    result = await registration_user.register_user()
    return result


@api_router.post("/send-email/registration")
async def send_email_endpoint(post_email: SendEmail,
                              db: Session = Depends(get_db)):
    result = await send_email(post_email, db)
    return result


@api_router.post("/verify-email/registration")
async def verify_code_endpoint(check: CheckCode,
                               db: Session = Depends(get_db)):
    result = await verification_code(check, db)
    return result


@api_router.post("/token")
async def login_for_access_token_endpoint(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await authenticate_user(form_data)
    return result


@api_router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    user_id = str(current_user.id)
    redis_client_for_cache.delete(user_id)
    return {"message": "Logged out successfully and cache cleared"}


@api_router.put("/change-password")
async def change_password_endpoint(new_password: ChangePassword,
                                   current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    changing_password = ChangingPassword(new_password, current_user, db)
    result = await changing_password.change_password()
    return result


@api_router.post("/send-email/password")
async def send_email_forgotten_password_endpoint(email_send: SendEmail):
    result = await send_email_forgotten_password(email_send)
    return result


@api_router.post("/verify-email/password")
async def reset_password_endpoint(verify_new_password: VerifyAndNewPassword):
    result = await reset_password(verify_new_password)
    return result


@api_router.put("/activate-status")
async def activate_user_endpoint(current_user: User = Depends(get_current_user),
                                 db: Session = Depends(get_db)):
    activate_user = UserActivateStatus(current_user, db)
    result = await activate_user.activate_status()
    return result


@api_router.put("/deactivate-status")
async def deactivate_user_endpoint(current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    deactivate_user = UserDeactivateStatus(current_user, db)
    result = await deactivate_user.deactivate_status()
    return result


@api_router.post("/new-employee")
async def new_employee_endpoint(create_data: NewEmployee,
                                current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    employee_manager = EmployeeManager(current_user, db)
    result = await employee_manager.add_employee(create_data)
    return result


@api_router.put("/update-employee")
async def update_position_employee_endpoint(update_data: UpdatePosition,
                                            current_user: User = Depends(get_current_user),
                                            db: Session = Depends(get_db)):
    employee_manager = EmployeeManager(current_user, db)
    result = await employee_manager.update_employee_position(update_data)
    return result


@api_router.delete("/delete-employee")
async def delete_employee_endpoint(delete_data: DeleteEmployee,
                                   current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    employee_manager = EmployeeManager(current_user, db)
    result = await employee_manager.delete_employee(delete_data)
    return result


@api_router.get("/get-employee")
async def get_employee_endpoint(current_user: User = Depends(get_current_user),
                                db: Session = Depends(get_db)):
    employee_manager = EmployeeManager(current_user, db)
    result = await employee_manager.get_employee_position()
    return result


@api_router.post("/create-food")
async def create_food_endpoint(create_data: CreateFood,
                               current_user: User = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    food_manager = FoodManager(current_user, db)
    result = await food_manager.create_food(create_data)
    return result


@api_router.put("/update-food")
async def update_food_endpoint(update_data: UpdateFood,
                               current_user: User = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    food_manager = FoodManager(current_user, db)
    result = await food_manager.update_food(update_data)
    return result


@api_router.delete("/delete-food")
async def delete_food_endpoint(delete_data: DeleteFood,
                               current_user: User = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    food_manager = FoodManager(current_user, db)
    result = await food_manager.delete_food(delete_data)
    return result


@api_router.get("/get-all-assortment")
@cache(expire=30, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_all_assortment_endpoint(current_user: User = Depends(get_current_user),
                                      db: Session = Depends(get_db)):
    food_manager = FoodManager(current_user, db)
    result = await food_manager.get_food()
    return result


@api_router.post("/create-set-food")
async def create_set_food_endpoint(create_data: FoodSetCreate,
                                   current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    food_set_manager = FoodSetManager(current_user, db)
    result = await food_set_manager.create_food_set(create_data)
    return result


@api_router.put("/update-set-food")
async def update_set_food_endpoint(update_data: FoodSetUpdate,
                                   current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    food_set_manager = FoodSetManager(current_user, db)
    result = await food_set_manager.update_food_set(update_data)
    return result


@api_router.delete("/delete-set-food")
async def update_set_food_endpoint(delete_data: FoodSetDelete,
                                   current_user: User = Depends(get_current_user),
                                   db: Session = Depends(get_db)):
    food_set_manager = FoodSetManager(current_user, db)
    result = await food_set_manager.delete_food_set(delete_data)
    return result


@api_router.get("/get-all-food-sets")
@cache(expire=30, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_all_food_sets_endpoint(current_user: User = Depends(get_current_user),
                                     db: Session = Depends(get_db)):
    food_set_manager = FoodSetManager(current_user, db)
    result = await food_set_manager.get_food_set()
    return result


@api_router.post("/add-favorite-food")
async def add_favorite_food_endpoint(food_data: AddFavoriteFood, current_user: User = Depends(get_current_user)):
    result = await add_favorite_food(food_data, current_user)
    return result


@api_router.delete("/delete-favorite-food")
async def delete_favorite_food_endpoint(food_data: DeleteFavoriteFood, current_user: User = Depends(get_current_user)):
    result = await delete_favorite_food(food_data, current_user)
    return result


@api_router.get("/get-favorite-food")
@cache(expire=5, coder=JsonCoder, key_builder=user_cache_key_builder)
async def get_favorite_food_endpoint(current_user: User = Depends(get_current_user)):
    result = await list_favorite_foods(current_user)
    return result


@api_router.post("/create-payment")
async def create_payment_endpoint(payment_data: PaymentCreate, current_user: User = Depends(get_current_user)):
    result = await create_payment(payment_data, current_user)
    return result


@api_router.put("/update-payment")
async def update_payment_endpoint(payment_data: PaymentUpdate, current_user: User = Depends(get_current_user)):
    result = await update_payment(payment_data, current_user)
    return result


@api_router.delete("/delete-payment")
async def delete_payment_endpoint(payment_data: PaymentDelete, current_user: User = Depends(get_current_user)):
    result = await delete_payment(payment_data, current_user)
    return result


@api_router.get("/redis-all/information")
async def read_all_redis_data_endpoint():
    result = await read_all_redis_data()
    return result


@api_router.get("/redis-cache/all-information")
async def read_all_redis_cache_data_endpoint():
    result = await read_all_redis_data_for_cache()
    return result


@api_router.get("/me")
@cache(expire=5, coder=JsonCoder, key_builder=user_cache_key_builder)
async def read_users_me(current_user: User = Depends(get_current_user)):
    result = await info_about_me(current_user)
    return result


@api_router.get("/test")
@cache(expire=180)
async def read_users_test(text: str):
    return text
