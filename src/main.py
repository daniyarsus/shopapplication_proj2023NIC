from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import redis
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from src.services.email_verification import send_email, verification_code
from src.services.redis_utils import init_redis, close_redis
from src.services.postgres_utils import init_postgres, close_postgres
from src.validators.schemas import *
from src.settings.config import SessionLocal, ACCESS_TOKEN_EXPIRE_MINUTES, REDIS_URL
from src.database.models import User
from src.auth.current_user import get_current_user
from src.auth.register_user import register_user
from src.auth.token import create_access_token


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
    session = SessionLocal()
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Verify code"
        )

    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


#@app.put("/activate")
#async def activate_user_endpoint(current_user: User = Depends(get_current_user)):
#    result = await activate_user(current_user)
#    return result
#
#
#@app.put("/deactivate")
#async def deactivate_user_endpoint(current_user: User = Depends(get_current_user)):
#    result = await deactivate_user(current_user)
#    return result


@app.put("/user/activate")
async def activate_user(current_user: User = Depends(get_current_user)):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    db.add(user)  # Добавляем объект пользователя обратно в сессию для обновления
    db.commit()  # Фиксируем изменения в базе данных
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
    db.add(user)  # Добавляем объект пользователя обратно в сессию для обновления
    db.commit()  # Фиксируем изменения в базе данных
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

