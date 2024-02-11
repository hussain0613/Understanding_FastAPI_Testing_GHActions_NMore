from app import app_factory
from settings import Settings

app = app_factory(Settings("sqlite:///./test.db"))
