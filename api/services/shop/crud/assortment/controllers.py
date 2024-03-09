from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.services.shop.models import AssortmentFood
from api.services.auth.models import User


class AssortmentsManager:
    def __init__(self, db: AsyncSession, current_user: User) -> None:
        self.db = db
        self.current_user = current_user

    async def get_all_food(self):
        try:
            query = select(AssortmentFood).where(AssortmentFood.is_active == True)
            result = await self.db.execute(query)
            food = result.scalars().all()

            return food

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
