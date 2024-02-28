from datetime import datetime

from sqlalchemy import String, Integer
from sqlalchemy.orm import (Mapped,
                            mapped_column)
from sqlalchemy.dialects.postgresql import ARRAY

from api.database.database import Base


class AssortmentBaseFood(Base):
    __tablename__ = "assortment_base_foods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(25), index=True)
    type: Mapped[str] = mapped_column(default=None)
    description: Mapped[str] = mapped_column(String(512), index=True)
    price: Mapped[int] = mapped_column(index=True)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)


class AssortmentSetFood(Base):
    __tablename__ = "assortment_set_foods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    foods_id: Mapped[list] = mapped_column(ARRAY(Integer), index=True)
    name: Mapped[str] = mapped_column(String(25), index=True)
    description: Mapped[str] = mapped_column(String(512), index=True)
    price: Mapped[int] = mapped_column(index=True)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
