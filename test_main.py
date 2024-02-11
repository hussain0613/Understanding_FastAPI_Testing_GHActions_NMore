from fastapi.testclient import TestClient
from app import app_factory
from schemas import ItemBase, ItemResponse
from init_db import Base
from sqlalchemy import create_engine
from settings import Settings

settings: Settings = Settings("sqlite:///./test.db")
engine = create_engine(settings.database_url)

app = app_factory(settings)

client = TestClient(app)


items_to_create = [
    ItemResponse(name="Foo", description="Fighters", price=100.0, id=1),
    ItemResponse(name="Bar", description="Brawlers", price=200.0, id=2),
    ItemResponse(name="Baz", description="Blasters", price=300.0, id=3),
]


def test_drop_db():
    Base.metadata.drop_all(engine)
    print("Database dropped!")


def test_init_db():
    Base.metadata.create_all(engine)
    print("Database initialized!")


def test_create_item():
    response = client.post(
        "/items/",
        json=items_to_create[0].model_dump()
    )
    print(response.json())
    print(response)
    print(response.status_code)
    assert response.status_code == 201
    assert response.json() == items_to_create[0].model_dump()


def test_create_item_2():
    response = client.post(
        "/items/",
        json=items_to_create[1].model_dump()
    )
    assert response.status_code == 201
    assert response.json() == items_to_create[1].model_dump()


def test_create_item_3():
    response = client.post(
        "/items/",
        json=items_to_create[2].model_dump()
    )
    assert response.status_code == 201
    assert response.json() == items_to_create[2].model_dump()


def test_create_duplicate_item():
    response = client.post(
        "/items/",
        json=items_to_create[0].model_dump()
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "Item already exists"}


def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json() == items_to_create[0].model_dump()


def test_read_item_2():
    response = client.get("/items/2")
    assert response.status_code == 200
    assert response.json() == items_to_create[1].model_dump()


def test_read_item_3():
    response = client.get("/items/3")
    assert response.status_code == 200
    assert response.json() == items_to_create[2].model_dump()


def test_read_item_not_found():
    response = client.get("/items/4")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "items": [
            items_to_create[0].model_dump(),
            items_to_create[1].model_dump(),
            items_to_create[2].model_dump(),
        ],
        "total_length": 3,
    }


def test_clean_up():
    Base.metadata.drop_all(engine)
    import os
    os.remove("./test.db")
    print("Database dropped!")

