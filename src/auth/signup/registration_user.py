from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.models import User
from src.validators.schemas import UserRegister


class RegistrationUser:
    def __init__(self, user_in, db):
        self.user_in = user_in
        self.db = db

    async def _check_existing_user(self):
        existing_user = self.db.query(User).filter(User.username == self.user_in.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User is registered")

    async def register_user(self):
        await self._check_existing_user()

        user = User(
            name=self.user_in.name,
            lastname=self.user_in.lastname,
            email=self.user_in.email,
            phone_number=self.user_in.phone_number,
            username=self.user_in.username,
            password=self.user_in.password,
            image_bs64=self.user_in.image_bs64
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return {"message": "Successfully registered"}

