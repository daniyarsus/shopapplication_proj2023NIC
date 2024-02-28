from typing import Annotated, List, Union

from pydantic import (BaseModel,
                      Field)


class AssortmentBaseFood(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=25)]
    type: Annotated[str, Field(min_length=1, max_length=25)]
    description: Annotated[str, Field(min_length=1, max_length=512)]
    price: Annotated[int, Field(...)]


class CreateAssortmentBaseFood(AssortmentBaseFood):
    pass


class UpdateAssortmentBaseFood(AssortmentBaseFood):
    id: Annotated[int, Field(...)]


class DeleteAssortmentBaseFood(AssortmentBaseFood):
    id: Annotated[int, Field(...)]


class AssortmentSetFood(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=25)]
    foods_id: Annotated[Union[int, List[int]], Field(...)]
    description: Annotated[str, Field(min_length=1, max_length=512)]
    price: Annotated[int, Field(...)]


class CreateAssortmentSetFood(AssortmentSetFood):
    pass


class UpdateAssortmentSetFood(AssortmentSetFood):
    id: Annotated[int, Field(...)]


class DeleteAssortmentSetFood(AssortmentSetFood):
    id: Annotated[int, Field(...)]

