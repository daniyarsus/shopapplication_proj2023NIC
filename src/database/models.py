from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Database setup
DATABASE_URL = "sqlite:///./test.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    shop_id = Column(Integer, ForeignKey('shops.id'))
    shop = relationship("Shop")


class Shop(Base):
    __tablename__ = "shops"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


# Dish model
class Dish(Base):
    __tablename__ = "dishes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    shop_id = Column(Integer, ForeignKey('shops.id'))
    shop = relationship("Shop")


# Queue model
class QueueItem(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    is_order_ready = Column(Boolean, default=False)
    user = relationship("User")
    shop = relationship("Shop")


# Create tables
Base.metadata.create_all(bind=engine)


