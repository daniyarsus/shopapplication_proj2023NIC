from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.services.auth.models import User
from api.services.auth.signup.schemas import SignupSchema, SignupEmailSend, SignupEmailVerify


class SignupManager:
    def __init__(self, form_data: SignupSchema, db: AsyncSession):
        self.form_data = form_data
        self.db = db

    async def _check_existing_user(self):
        query = select(User).where(User.username == self.form_data.username)
        existing_user = await self.db.execute(query)
        if existing_user:
            raise HTTPException(status_code=400, detail="User is registered")

    async def register_user(self):
        #await self._check_existing_user()

        user = User(
            name=self.form_data.name,
            lastname=self.form_data.lastname,
            email=self.form_data.email,
            phone=self.form_data.phone,
            username=self.form_data.username,
            password=self.form_data.password
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return {"message": "Successfully registered"}


class SignupSendEmailManager:
    def __init__(self, form_data: SignupEmailSend, db: AsyncSession):
        self.form = form_data
        self.db = db
