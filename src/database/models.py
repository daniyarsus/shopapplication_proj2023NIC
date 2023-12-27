from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.settings.config import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    image_url = Column(String, default=None)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=None)
    verification_code = Column(String, default=None)


Base.metadata.create_all(engine)

