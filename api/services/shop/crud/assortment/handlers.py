from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User

from api.services.shop.crud.assortment.controllers import AssortmentsManager


router = APIRouter()


@router.get("/get_all_assortments")
async def get_all_assortments(current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    assortments_manager = AssortmentsManager(current_user=current_user,
                                             db=db)
    result = await assortments_manager.get_all_food()
    return result
