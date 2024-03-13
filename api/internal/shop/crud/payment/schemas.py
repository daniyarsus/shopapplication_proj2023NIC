from typing import Annotated, List

from pydantic import (BaseModel,
                      Field)


class Payment(BaseModel):
    class Config:
        from_attributes = True


class CreatePayment(Payment):
    user_id: Annotated[int, Field(...)]
    summ: Annotated[int, Field(...)]
    foods_id: Annotated[List, Field(...)]
    place: Annotated[str, Field(...)]
    qr_code: Annotated[str, Field(...)]
    is_verified: Annotated[bool, Field(...)]
    is_received: Annotated[bool, Field(...)]


class UpdatePayment(Payment):
    id: Annotated[int, Field(...)]
    user_id: Annotated[int, Field(...)]
    summ: Annotated[int, Field(...)]
    foods_id: Annotated[List, Field(...)]
    place: Annotated[str, Field(...)]
    qr_code: Annotated[str, Field(...)]
    is_verified: Annotated[bool, Field(...)]
    is_received: Annotated[bool, Field(...)]


class DeletePayment(Payment):
    id: Annotated[int, Field(...)]
