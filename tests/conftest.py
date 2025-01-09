import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base, get_db
from app.config import settings
from app.models import *
from app.main import app


@pytest.fixture(scope="session")
def engine():
    database_url = settings.TEST_DATABASE_URL
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


@pytest.fixture(scope="function")
def client(session):
    app.dependency_overrides[get_db] = lambda: session
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_db)
