from fastapi import Depends, HTTPException

from src.settings.config import SessionLocal
from src.database.models import User


async def register_user(user_in):
    session = SessionLocal()
    existing_user = session.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is registered")
    user = User(
        name=user_in.name,
        lastname=user_in.lastname,
        email=user_in.email,
        phone_number=user_in.phone_number,
        username=user_in.username,
        password=user_in.password
    )
    session.add(user)
    session.commit()
    return {"message": "Successfully registered"}

