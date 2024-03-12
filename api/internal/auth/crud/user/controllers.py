from datetime import datetime

from fastapi import HTTPException, status

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from api.internal.auth.models import User
from api.internal.auth.crud.user import schemas


class UserManager:
    def __init__(self, current_user: User, db: AsyncSession):
        self.current_user = current_user
        self.db = db

    async def create_user(self, create_data: schemas.CreateUser):
        try:
            user = User(
                name=create_data.name,
                lastname=create_data.lastname,
                email=create_data.email,
                phone=create_data.phone,
                username=create_data.username,
                password=create_data.password,
                is_active=create_data.is_active,
                is_verified=create_data.is_verified,
                permission=create_data.permission
            )

            self.db.add(user)
            await self.db.commit()

            return {"message": "User created successfully", "food_id": user.id}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def update_user(self, update_data: schemas.UpdateUser):
        try:
            query = select(User).where(User.id == update_data.id)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()

            if user:
                user.name = create_data.name,
                user.lastname = create_data.lastname,
                user.email = create_data.email,
                user.phone = create_data.phone,
                user.username = create_data.username,
                user.password = create_data.password,
                user.is_active = create_data.is_active,
                user.is_verified = create_data.is_verified,
                user.permission = create_data.permission

                await self.db.commit()
                await self.db.refresh(user)

                return {"message": "User updated successfully", "user_id": user.id}

            else:
                raise HTTPException(status_code=404, detail="User not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_user(self, delete_data: schemas.DeleteUser):
        try:
            query = select(User).where(User.id == delete_data.id)
            result = await self.db.execute(query)
            user = result.scalar_one_or_none()

            if user:
                await self.db.delete(user)
                await self.db.commit()

                return {"message": "User deleted successfully", "user_id": delete_data.id}

            else:
                raise HTTPException(status_code=404, detail="User not found")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def get_all_user(self):
        query = select(User)
        result = await self.db.execute(query)
        user = result.scalars().all()
        user_data = [
            {"id": user.id,
             "name": user.name,
             "lastname": user.lastname,
             "email": user.email,
             "phone": user.phone,
             "username": user.username,
             "password": user.password,
             "is_active": user.is_active,
             "is_verified": user.is_verified,
             "permission": user.permission
             }
            for user in user
        ]

        return user_data
