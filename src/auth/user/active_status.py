from fastapi import HTTPException

from src.database.models import User


class UserActivateStatus:
    def __init__(self, current_user, db):
        self.current_user = current_user
        self.db = db

    async def check_user(self):
        user_db = self.db.query(User).filter(User.id == self.current_user.id).first()

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return user_db

    async def activate_status(self):
        user_db = await self.check_user()

        user_db.is_active = True
        self.db.add(user)
        self.db.commit()
        self.db.close()

        return {"message": "User activated successfully"}


class UserDeactivateStatus:
    def __init__(self, current_user, db):
        self.current_user = current_user
        self.db = db

    async def check_user(self):
        user_db = self.db.query(User).filter(User.id == self.current_user.id).first()

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return user_db

    async def deactivate_status(self):
        user_db = await self.check_user()

        user_db.is_active = False
        self.db.add(user)
        self.db.commit()
        self.db.close()

        return {"message": "User deactivated successfully"}

