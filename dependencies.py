from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from settings import Settings


def get_db_engine_factory(settings: Settings):
    engine: Engine = create_engine(settings.database_url)
    def get_db_engine() -> Engine:
        return engine
    return get_db_engine

get_db_engine = get_db_engine_factory(Settings())
