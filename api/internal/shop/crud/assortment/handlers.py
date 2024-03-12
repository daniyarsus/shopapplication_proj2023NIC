from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.internal.auth.models import User
from api.internal.shop.crud.assortment import schemas
from api.internal.shop.crud.assortment.controllers import FoodManager

shop_router = APIRouter()


@shop_router.post("/create-food")
@permission_required(2)
async def create_food_endpoint(create_data: schemas.CreateAssortmentFood = Depends(),
                               db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    food_manager = FoodManager(current_user=current_user,
                               db=db)
    result = await food_manager.create_food(create_data=create_data)
    return result


@shop_router.put("/update-food")
@permission_required(2)
async def update_food_endpoint(update_data: schemas.UpdateAssortmentFood = Depends(),
                               db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    food_manager = FoodManager(current_user=current_user,
                               db=db)
    result = await food_manager.update_food(update_data=update_data)
    return result


@shop_router.delete("/delete-food")
@permission_required(2)
async def delete_food_endpoint(delete_data: schemas.DeleteAssortmentFood = Depends(),
                               db: AsyncSession = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    food_manager = FoodManager(current_user=current_user,
                               db=db)
    result = await food_manager.delete_food(delete_data=delete_data)
    return result


@shop_router.get("/get-all-food")
@permission_required(1)
async def get_base_food_endpoint(db: AsyncSession = Depends(get_db),
                                 current_user: User = Depends(get_current_user)
                                 ):
    food_manager = FoodManager(current_user=current_user,
                               db=db)
    result = await food_manager.get_all_food()
    return result
