from fastapi import Depends, HTTPException, status

from src.database.models import User


class ChangingPassword:
    def __init__(self, new_password, current_user, db):
        self.new_password = new_password
        self.current_user = current_user
        self.db = db

    async def _check_user(self):
        user_db = self.db.query(User).filter(User.id == self.current_user.id).first()

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return user_db

    async def change_password(self):
        user_db = await self._check_user()

        if user_db.password != self.new_password.old_password:
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        user_db.password = self.new_password.new_password
        self.db.commit()

        return user_db
