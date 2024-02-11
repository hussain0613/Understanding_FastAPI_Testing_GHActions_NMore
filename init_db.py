from sqlalchemy import create_engine
from models import Base
from settings import Settings

engine = create_engine(Settings().database_url)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
