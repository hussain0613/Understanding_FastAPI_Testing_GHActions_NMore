from fastapi import FastAPI, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine

from models import Item
from schemas import ItemBase, ItemResponse, ItemsResponse
from settings import Settings
from dependencies import get_db_engine, get_db_engine_factory

router = APIRouter()


@router.post("/items/", status_code=201)
async def create_item(item: ItemBase, engine: Engine = Depends(get_db_engine)) -> ItemResponse:
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


@router.get("/items/{item_id}")
async def read_item(item_id: int, engine: Engine = Depends(get_db_engine)) -> ItemResponse:
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return ItemResponse.model_validate(item, from_attributes=True)


@router.get("/items/")
async def read_items(skip: int = 0, limit: int = None, engine: Engine = Depends(get_db_engine)) -> ItemsResponse:
    with Session(engine) as session:
        items_query = session.query(Item)
        items_count = items_query.count()
        items = session.query(Item).offset(skip).limit(limit).all()
        
        items_responses = [ItemResponse.model_validate(item, from_attributes=True) for item in items]
        return ItemsResponse(items=items_responses, total_length=items_count)



def app_factory(settings: Settings, router: APIRouter = router) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db_engine] = get_db_engine_factory(settings)
    return app


