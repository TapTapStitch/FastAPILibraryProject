import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base
from dotenv import dotenv_values
from app.models import *  # To ensure all models are imported


@pytest.fixture(scope="session")
def engine():
    database_url = dotenv_values(".env").get("TEST_DATABASE_URL")
    if not database_url:
        raise ValueError("TEST_DATABASE_URL is not set in the environment variables.")
    engine = create_engine(database_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope="function")
def session(engine):
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
