from typing import Annotated, List

from pydantic import (BaseModel,
                      Field)


class BasePayment(BaseModel):
    class Config:
        from_attributes = True


class PaymentCreate(BasePayment):
    foods_id: List[int]
    place: Annotated[str, Field(...)] = 'shop'
