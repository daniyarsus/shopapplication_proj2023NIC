from fastapi import HTTPException

from src.database.models import User
from src.settings.config import SessionLocal
from src.auth.current_user import get_current_user


async def activate_user():
    pass


async def deactivate_user(user: User):
    db = SessionLocal()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}

