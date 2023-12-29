from fastapi import HTTPException

from src.database.models import User
from src.settings.config import SessionLocal


async def activate_user_status(current_user):
    db = SessionLocal()

    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = True
    db.add(user)
    db.commit()
    db.close()

    return {"message": "User activated successfully"}


async def deactivate_user_status(current_user):
    db = SessionLocal()

    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.add(user)
    db.commit()
    db.close()

    return {"message": "User deactivated successfully"}

