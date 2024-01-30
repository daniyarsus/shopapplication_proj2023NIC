from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

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


class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_code = Column(String, default=None)
    email_verified_at = Column(DateTime, default=None)
    password_code = Column(String, default=None)
    password_verified_at = Column(DateTime, default=None)


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    position = Column(String, default="employee", index=True)


class Assortment(Base):
    __tablename__ = "assortments"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer, index=True)
    image_url = Column(String, default=None)


class FavoriteFood(Base):
    __tablename__ = "favorite_foods"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    food_id = Column(Integer, ForeignKey("assortments.id"))


class FoodSet(Base):
    __tablename__ = "food_sets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer, index=True)
    image_url = Column(String, default=None)


#class Payments(Base):
#    __tablename__ = "payments"
#
#    id = Column(Integer, primary_key=True, index=True)
#    buyer_id = Column(Integer, ForeignKey("users.id"))
#    foods_id = Column(Integer)


Base.metadata.create_all(engine)

