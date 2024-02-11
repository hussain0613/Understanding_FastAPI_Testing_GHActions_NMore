from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import Item
from schemas import ItemBase
from init_db import engine

app = FastAPI()



@app.post("/items/")
async def create_item(item: ItemBase):
    with Session(engine) as session:
        db_item = Item(**item.model_dump())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        items = session.query(Item).offset(skip).limit(limit).all()
        return items
