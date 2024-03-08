from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils.decorators.permission import permission_required
from api.utils.dependencies.current_user import get_current_user
from api.utils.dependencies.db import get_db

from api.services.auth.models import User

from api.services.shop.crud.favorite_food.controllers import FavoriteFoodManager
from api.services.shop.crud.favorite_food import schemas


router = APIRouter()


@router.post("/add-favorite-food")
async def add_favorite_food_endpoint(create_data: schemas.AddFavoriteFood = Depends(),
                                     db: AsyncSession = Depends(get_db),
                                     current_user: User = Depends(get_current_user)
                                     ):
    favorite_food_manager = FavoriteFoodManager(current_user=current_user,
                                                db=db)
    result = await favorite_food_manager.add_favorite_food(create_data=create_data)
    return result


@router.delete("/remove-favorite-food")
async def remove_favorite_food_endpoint(delete_data: schemas.DeleteFavoriteFood = Depends(),
                                        db: AsyncSession = Depends(get_db),
                                        current_user: User = Depends(get_current_user)
                                        ):
    favorite_food_manager = FavoriteFoodManager(current_user=current_user,
                                                db=db)
    result = await favorite_food_manager.remove_favorite_food(delete_data=delete_data)
    return result


@router.get("/get-all-favorite-food")
async def get_all_favorite_food_endpoint(current_user: User = Depends(get_current_user),
                                         db: AsyncSession = Depends(get_db)
                                         ):
    favorite_food_manager = FavoriteFoodManager(current_user=current_user,
                                                db=db)
    result = await favorite_food_manager.get_all_favorite_food()
    return result
