from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from src.config import settings
engine = create_engine(settings.database_url)


class Base(DeclarativeBase):
    pass


def get_session():
    with session_factory() as session:
        yield session


session_factory = sessionmaker(engine)
