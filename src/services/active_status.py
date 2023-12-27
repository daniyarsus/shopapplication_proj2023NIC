from fastapi import HTTPException

from src.database.models import User
from src.settings.config import SessionLocal
from src.auth.current_user import get_current_user


async def activate_user(user: User, current_user: User = Depends(get_current_user())):
    db = SessionLocal()
    status = cu
    #db.add(current_user.is_active = True)
    db.commit()
    return {"message": "User activated successfully"}


async def deactivate_user(user: User):
    db = SessionLocal()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.is_active = False
    db.commit()
    return {"message": "User deactivated successfully"}

