from fastapi import Depends, HTTPException, status, Response, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from src.config.dependencies import get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from config.settings import SessionLocal, redis_client
from schemas import UserIn, Logout, UpdatePassword
from src.database.models import *


auth_router = APIRouter()


# User endpoints
@auth_router.post("/register")
async def register(user_in: UserIn):
    session = SessionLocal()

    # Проверка существования пользователя с указанным именем
    existing_user = session.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is registered")

    # Создание нового пользователя
    user = User(username=user_in.username, password=user_in.password)
    session.add(user)
    session.commit()

    return {"username": user.username}


@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session = SessionLocal()
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout")
async def logout(logout: Logout, current_user: User = Depends(get_current_user)):
    access_token = logout.access_token
    redis_client.delete(access_token)  # Удаление сессии из Redis
    response = Response()
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


@auth_router.put("/change_password")
async def change_password(new_password: UpdatePassword, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Проверяем старый пароль
    if current_user.password != new_password.old_password:
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # Асинхронная функция для изменения пароля пользователя
    async def update_password(user_id: int, password: str):
        user_db = session.query(User).filter(User.id == user_id).first()
        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")
        user_db.password = password
        session.commit()

    # Изменяем пароль текущего пользователя
    await update_password(current_user.id, new_password.new_password)

    session.close()
    return {"message": "Password updated successfully"}