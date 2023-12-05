from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import jwt
from datetime import datetime, timedelta
import asyncio
from fastapi.middleware.cors import CORSMiddleware

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

    # Новый столбец, который будет хранить идентификатор магазина, к которому привязан пользователь
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


# Pydantic models
class UserIn(BaseModel):
    username: str
    password: str


class ShopCreate(BaseModel):
    name: str


class DishCreate(BaseModel):
    name: str
    shop_id: int


class QueueAdd(BaseModel):
    dish_id: int
    shop_id: int


# Security and authentication
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Helper functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user



# Функция для получения всех пользователей из базы данных
def get_all_users():
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# User endpoints
@app.post("/register")
async def register(user_in: UserIn):
    session = SessionLocal()

    # Проверка существования пользователя с указанным именем
    existing_user = session.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User is registered")

    # Создание нового пользователя
    user = User(username=user_in.username, password=user_in.password)
    session.add(user)
    session.commit()

    return {"username": user.username}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    session = SessionLocal()
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


# Shop endpoints
@app.post("/shop/create")
async def create_shop(shop_create: ShopCreate, current_user: User = Depends(get_current_user)):
    session = SessionLocal()

    # Проверка, является ли текущий пользователь авторизованным
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    existing_shop = session.query(Shop).filter(Shop.name == shop_create.name).first()
    if existing_shop:
        raise HTTPException(status_code=400, detail="Shop already exists")

    shop = Shop(name=shop_create.name)
    session.add(shop)
    session.commit()
    return {"shop_id": shop.id, "name": shop.name}


# Dish endpoints
@app.post("/dish/{shop_name}/create")
async def create_dish(shop_name: str, dish_create: DishCreate, current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.name == shop_name).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Проверяем, привязан ли текущий пользователь к выбранному магазину
    if current_user.shop_id != shop.id:
        raise HTTPException(status_code=403, detail="You are not allowed to create dishes for this shop")

    dish = Dish(name=dish_create.name, shop_id=shop.id)
    session.add(dish)
    session.commit()
    return {"dish_id": dish.id, "name": dish.name, "shop_id": dish.shop_id}


# Queue endpoints
@app.post("/shop/{shop_name}/queue/add")
async def add_to_queue(shop_name: str, queue_add: QueueAdd, current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.name == shop_name).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")

    # Проверяем, существует ли блюдо с указанным ID в выбранном магазине
    dish = session.query(Dish).filter(Dish.id == queue_add.dish_id, Dish.shop_id == shop.id).first()
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    # Создаем запись в очереди
    queue_item = QueueItem(user_id=current_user.id, shop_id=shop.id)
    session.add(queue_item)
    session.commit()
    session.refresh(queue_item)
    return {"queue_id": queue_item.id, "message": "You've been added to the queue"}


@app.post("/shop/{shop_name}/queue/{queue_id}/ready")
async def order_ready(shop_name: str, queue_id: int, current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.name == shop_name).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id, QueueItem.shop_id == shop.id).first()
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")

    # Проверяем, является ли текущий пользователь владельцем заказа в очереди
    if queue_item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to mark this order as ready")

    queue_item.is_order_ready = True
    session.commit()
    return {"queue_id": queue_id, "message": "Order is ready for pickup"}


@app.get("/shop/{shop_name}/queue/{queue_id}/status")
async def check_queue_status(shop_name: str, queue_id: int):
    session = SessionLocal()
    shop = session.query(Shop).filter(Shop.name == shop_name).first()
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id, QueueItem.shop_id == shop.id).first()
    if not queue_item:
        raise HTTPException(status_code=404, detail="Queue item not found")
    return {"queue_id": queue_id, "is_order_ready": queue_item.is_order_ready}


# WebSocket endpoint for real-time notifications
@app.websocket("/ws/shop/{shop_name}/queue/{queue_id}")
async def websocket_endpoint(websocket: WebSocket, shop_name: str, queue_id: int):
    await websocket.accept()
    session = SessionLocal()
    try:
        while True:
            shop = session.query(Shop).filter(Shop.name == shop_name).first()
            if not shop:
                raise HTTPException(status_code=404, detail="Shop not found")
            queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id, QueueItem.shop_id == shop.id).first()
            if queue_item and queue_item.is_order_ready:
                await websocket.send_json({"queue_id": queue_id, "message": "Your order is ready"})
            break
        await asyncio.sleep(1)  # Check every second
    finally:
        await websocket.close()
        session.close()

# Эндпоинт для вывода всех данных из таблицы Users
@app.get("/users_all")
async def read_all_users():
    users = get_all_users()
    return users