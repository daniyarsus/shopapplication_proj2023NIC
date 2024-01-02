from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from src.auth.signup.register_verification import send_email, verification_code
from src.auth.signup.registration_user import register_user
from src.services.redis_utils.redis_status import init_redis, close_redis
from src.services.postgres_utils import init_postgres, close_postgres
from src.validators.schemas import *
from src.settings.config import SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES, REDIS_URL
from src.database.models import User
from src.auth.user.current_user import get_current_user
from src.auth.signin.token import create_access_token
from src.auth.signin.login_user import authenticate_user
from src.auth.password.changing_password import change_user_password
from src.auth.password.password_verification import send_email_forgotten_password, reset_password
from src.auth.user.active_status import activate_user_status, deactivate_user_status
from src.services.redis_utils.redis_users import read_all_redis_data
from src.shop_development.position_settings import add_employee, delete_employee, update_position_employee


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await authenticate_user(form_data)
    return result


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
async def update_position_employee_endpoint(upd_employee: UpdatePosition, current_user: User = Depends()):
    result = await update_position_employee(upd_employee, current_user)
    return result


@app.delete("/delete-employee")
async def delete_employee_endpoint(employee_data: DeleteEmployee, current_user: User = Depends(get_current_user)):
    result = await delete_employee(employee_data, current_user)
    return result


@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/redis-all-information")
async def read_all_redis_data_endpoint():
    result = await read_all_redis_data()
    return result


@app.on_event("startup")
async def startup_event():
    init_redis()
    await init_postgres()


@app.on_event("shutdown")
async def shutdown_event():
    close_redis()
    await close_postgres()

