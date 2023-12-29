from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import redis
from datetime import timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.auth.signup.register_verification import send_email, verification_code
from src.auth.signup.registration_user import register_user
from src.services.redis_utils import init_redis, close_redis
from src.services.postgres_utils import init_postgres, close_postgres
from src.validators.schemas import *
from src.settings.config import SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES, REDIS_URL
from src.database.models import User
from src.auth.user.current_user import get_current_user
from src.auth.signin.token import create_access_token
from src.auth.signin.login_user import authenticate_user
from src.auth.password.changing_password import change_user_password
from src.auth.password.password_verification import send_email_forgotten_password, reset_password
#from src.auth.active_status import activate_user, deactivate_user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/register")
async def register(user_in: UserRegister):
    result = await register_user(user_in)
    return result


@app.post("/send-email")
async def send_email_endpoint(post_email: SendEmail):
    result = await send_email(post_email)
    return result


@app.post("/verify")
async def verify_code_endpoint(check: CheckCode):
    result = await verification_code(check)
    return result


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    result = await authenticate_user(form_data)
    return result


@app.put("/change-password")
async def change_password(new_password: ChangePassword, current_user: User = Depends(get_current_user)):
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


@app.put("/user/activate")
async def activate_user(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    db.add(user)
    db.commit()
    db.close()

    return {"message": "User activated successfully"}


@app.put("/user/deactivate")
async def activate_user(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.add(user)
    db.commit()
    db.close()

    return {"message": "User deactivated successfully"}


@app.get("/user/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.get("/redis/all")
async def read_all_redis_data():
    try:
        client = redis.from_url(REDIS_URL)
        keys = client.keys('*')
        data = {}
        for key in keys:
            value = client.get(key)
            if value is not None:
                data[key.decode('utf-8')] = value.decode('utf-8')
        return data
    except Exception as e:
        return {"error": f"Failed to connect to Redis: {e}"}


@app.on_event("startup")
async def startup_event():
    init_redis()
    await init_postgres()


@app.on_event("shutdown")
async def shutdown_event():
    close_redis()
    await close_postgres()

