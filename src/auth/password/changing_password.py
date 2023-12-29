from fastapi import Depends, HTTPException, status

from src.settings.config import SessionLocal
from src.auth.user.current_user import get_current_user
from src.database.models import User


async def change_user_password(user_id: int, old_password: str, new_password: str):
    session = SessionLocal()
    user_db = session.query(User).filter(User.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверяем старый пароль
    if user_db.password != old_password:
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user_db.password = new_password
    session.commit()
    return user_db

