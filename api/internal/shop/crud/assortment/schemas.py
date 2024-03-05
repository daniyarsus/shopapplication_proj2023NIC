from typing import Annotated, List

from pydantic import (BaseModel,
                      Field)


class AssortmentFood(BaseModel):
    class Config:
        from_attributes = True


class CreateAssortmentFood(AssortmentFood):
    name: Annotated[str, Field(min_length=1, max_length=25)]
    type: Annotated[str, Field(min_length=1, max_length=25)]
    description: Annotated[str, Field(min_length=1, max_length=512)]
    price: Annotated[int, Field(...)]


class UpdateAssortmentFood(CreateAssortmentFood):
    id: Annotated[int, Field(...)]


class DeleteAssortmentFood(AssortmentFood):
    id: Annotated[int, Field(...)]
