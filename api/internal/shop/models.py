from typing import List

from datetime import datetime

from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey)
from sqlalchemy.orm import (Mapped,
                            mapped_column)
from sqlalchemy.dialects.postgresql import ARRAY

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


class FavoriteFood(Base):
    __tablename__ = "favorite_foods"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    food_id: Mapped[int] = mapped_column(ForeignKey('assortment_foods.id'), index=True)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    summ: Mapped[int] = mapped_column(index=True)
    foods_id = Column(ARRAY(Integer), index=True)
    place: Mapped[str] = mapped_column(default='shop', index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    qrcode: Mapped[str] = mapped_column(default='qrcode', index=True)
    is_verified: Mapped[bool] = mapped_column(default=False, index=True)
    is_received: Mapped[bool] = mapped_column(default=False, index=True)
