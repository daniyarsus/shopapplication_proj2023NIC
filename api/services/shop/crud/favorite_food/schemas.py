from typing import Annotated

from pydantic import (BaseModel,
                      Field)


class FavoriteFoodBase(BaseModel):
    id: Annotated[int, Field(...)]

    class Config:
        from_attributes = True


class AddFavoriteFood(FavoriteFoodBase):
    pass


class DeleteFavoriteFood(FavoriteFoodBase):
    pass
