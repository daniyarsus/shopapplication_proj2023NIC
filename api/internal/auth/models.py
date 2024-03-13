from datetime import datetime

from sqlalchemy.orm import (Mapped,
                            mapped_column)

from api.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    lastname: Mapped[str] = mapped_column(index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str] = mapped_column(unique=True, index=True)
    photo: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column(index=True)
    register_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    login_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    changed_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=True)
    permission: Mapped[int] = mapped_column(default=0)


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True)
    code_email: Mapped[str] = mapped_column(index=True)
    email_send_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    code_password: Mapped[str] = mapped_column(index=True)
    password_send_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
