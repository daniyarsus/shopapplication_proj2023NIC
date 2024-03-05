from datetime import datetime

from sqlalchemy import String, Integer
from sqlalchemy.orm import (Mapped,
                            mapped_column)

from api.database.database import Base


class AssortmentFood(Base):
    __tablename__ = "assortment_foods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(25), index=True)
    type: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(String(512), index=True)
    price: Mapped[int] = mapped_column(index=True)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
