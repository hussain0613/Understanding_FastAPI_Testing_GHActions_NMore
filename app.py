from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Item
from schemas import ItemBase, ItemResponse, ItemsResponse
from init_db import engine

app = FastAPI()



@app.post("/items/")
async def create_item(item: ItemBase) -> ItemResponse:
    with Session(engine) as session:
        db_item = Item(**item.model_dump())
        session.add(db_item)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=409, detail="Item already exists")

        session.refresh(db_item)
        return ItemResponse.model_validate(db_item, from_attributes=True)


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> ItemResponse:
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemResponse.model_validate(item, from_attributes=True)


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = None) -> ItemsResponse:
    with Session(engine) as session:
        items_query = session.query(Item)
        items_count = items_query.count()
        items = session.query(Item).offset(skip).limit(limit).all()
        
        items_responses = [ItemResponse.model_validate(item, from_attributes=True) for item in items]
        return ItemsResponse(items=items_responses, total_length=items_count)




