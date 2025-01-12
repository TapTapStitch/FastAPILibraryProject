import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base, get_db
from app.config import settings
from app.models import *
from app.main import app
from app.services.authorization import get_current_user


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


@pytest.fixture(scope="function")
def authorized_client(client, session):
    user = User(
        email="user@example.com",
        hashed_password="some_hashed_password",
        name="User",
        surname="User",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    app.dependency_overrides[get_current_user] = lambda: user
    yield client
    app.dependency_overrides.pop(get_current_user)
