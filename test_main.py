from fastapi.testclient import TestClient
from app import app_factory, get_db_engine
from schemas import ItemResponse
from init_db import Base
from sqlalchemy import create_engine
from settings import Settings

sqlite_db_file = "test.db"
settings: Settings = Settings(database_url=f"sqlite:///{sqlite_db_file}")
engine = create_engine(settings.database_url)

app = app_factory(settings)
app.dependency_overrides[get_db_engine] = lambda: engine
# if we use the factory function, then the `engine` object created by the `get_db_engine` function still be in the memory and will not be disposed of
# and we will not be able to delete the database file

client = TestClient(app)


items_to_create = [
    ItemResponse(name="Foo", description="Fighters", price=100.0, id=1),
    ItemResponse(name="Bar", description="Brawlers", price=200.0, id=2),
    ItemResponse(name="Baz", description="Blasters", price=300.0, id=3),
]

def test_engine_settings():
    assert settings.database_url == f"sqlite:///{sqlite_db_file}"
    assert sqlite_db_file == engine.url.database


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
    engine.dispose() # this is important to dispose of the engine object, so that the database file can be deleted
    
    import os
    os.remove(sqlite_db_file)
    print("Cleaned up!")


if __name__ == "__main__":
    test_engine_settings()
    test_drop_db()
    test_init_db()
    test_create_item()
    test_create_item_2()
    test_create_item_3()
    test_create_duplicate_item()
    test_read_item()
    test_read_item_2()
    test_read_item_3()
    test_read_item_not_found()
    test_read_items()
    test_clean_up()
    print("All tests passed!")

