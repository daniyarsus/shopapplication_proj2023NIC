from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (Mapped,
                            mapped_column)

from api.database.database import Base


class Employee(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(ForeignKey('users.name'))
    lastname: Mapped[str] = mapped_column(ForeignKey('users.lastname'))
    email: Mapped[str] = mapped_column(ForeignKey('users.email'))
    phone: Mapped[str] = mapped_column(ForeignKey('users.phone'))
    username: Mapped[str] = mapped_column(ForeignKey('users.username'))
    added_on: datetime = mapped_column(default=datetime.utcnow)
    changed_on: datetime = mapped_column(default=datetime.utcnow)
    #permisiion
