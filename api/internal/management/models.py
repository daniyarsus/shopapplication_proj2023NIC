from datetime import datetime

from sqlalchemy import (ForeignKey,
                        String)
from sqlalchemy.orm import (Mapped,
                            mapped_column)

from api.database.database import Base


class Employee(Base):
    __tablename__ = 'employees'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    username: Mapped[str] = mapped_column(String(25))
    added_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    permission: Mapped[int] = mapped_column()
