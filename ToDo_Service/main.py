from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Инициализация FastAPI
app = FastAPI()

# Создание подключения к SQLite
DATABASE_URL = "sqlite:///./todo.db"


# Создаем соединение с базой данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Создание базового класса для моделей
Base = declarative_base()

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель SQLAlchemy для задачи
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

# Pydantic модель для валидации данных
class ItemBase(BaseModel):
    title: str
    description: str
    completed: bool = False

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    class Config:
        orm_mode = True


# Создаём таблицы
Base.metadata.create_all(bind=engine)


@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    session = SessionLocal()
    db_item = Item(**item.dict())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    session.close()
    return db_item

@app.get("/items", response_model=list[ItemResponse])
async def read_items():
    session = SessionLocal()
    items = session.query(Item).all()
    session.close()
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    session.close()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    session = SessionLocal()
    db_item = session.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        session.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    db_item.title = item.title
    db_item.description = item.description
    db_item.completed = item.completed
    session.commit()
    session.refresh(db_item)
    session.close()
    
    return db_item

@app.delete("/items/{item_id}", response_model=dict)
async def delete_item(item_id: int):
    session = SessionLocal()
    item = session.query(Item).filter(Item.id == item_id).first()
    if item is None:
        session.close()
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    session.close()
    return {"ok": True}

