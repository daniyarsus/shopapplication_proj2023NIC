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

# Queue model
class QueueItem(Base):
    __tablename__ = "queue"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_order_ready = Column(Boolean, default=False)
    user = relationship("User")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserIn(BaseModel):
    username: str
    password: str

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

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Замените "*" на список разрешенных источников
    allow_credentials=True,
    allow_methods=["*"],  # Замените "*" на список разрешенных HTTP-методов
    allow_headers=["*"],  # Замените "*" на список разрешенных HTTP-заголовков
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

@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Queue endpoints
@app.post("/queue/add")
async def add_to_queue(current_user: User = Depends(get_current_user)):
    session = SessionLocal()
    queue_item = QueueItem(user_id=current_user.id)
    session.add(queue_item)
    session.commit()
    session.refresh(queue_item)
    return {"queue_id": queue_item.id, "message": "You've been added to the queue"}

@app.post("/queue/{queue_id}/ready")
async def order_ready(queue_id: int):
    session = SessionLocal()
    queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id).first()
    if queue_item is None:
        raise HTTPException(status_code=404, detail="Queue item not found")
    queue_item.is_order_ready = True
    session.commit()
    return {"queue_id": queue_id, "message": "Order is ready for pickup"}

@app.get("/queue/{queue_id}/status")
async def check_queue_status(queue_id: int):
    session = SessionLocal()
    queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id).first()
    if queue_item is None:
        raise HTTPException(status_code=404, detail="Queue item not found")
    return {"queue_id": queue_id, "is_order_ready": queue_item.is_order_ready}

# WebSocket endpoint for real-time notifications
@app.websocket("/ws/queue/{queue_id}")
async def websocket_endpoint(websocket: WebSocket, queue_id: int):
    await websocket.accept()
    session = SessionLocal()
    try:
        while True:
            queue_item = session.query(QueueItem).filter(QueueItem.id == queue_id).first()
            if queue_item and queue_item.is_order_ready:
                await websocket.send_json({"queue_id": queue_id, "message": "Your order is ready"})
            break
        await asyncio.sleep(1) # Check every second
    finally:
        await websocket.close()
        session.close()
