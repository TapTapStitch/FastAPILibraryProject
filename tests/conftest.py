import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Base, get_db
from app.config import settings
from app.models import *
from app.main import app
from app.services.authorization import get_current_user
from app.routers.api.v1.shared.depends import get_librarian_user, get_admin_user


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
        avatar_link="https://example.com/avatar.jpg",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    app.dependency_overrides[get_current_user] = lambda: user
    yield client
    app.dependency_overrides.pop(get_current_user)


@pytest.fixture(scope="function")
def authorized_librarian(client, session):
    librarian = User(
        email="librarian@example.com",
        hashed_password="some_hashed_password",
        name="Librarian",
        surname="Librarian",
        avatar_link="https://example.com/avatar.jpg",
        access_level=1,
    )
    session.add(librarian)
    session.commit()
    session.refresh(librarian)
    app.dependency_overrides[get_librarian_user] = lambda: librarian
    yield client
    app.dependency_overrides.pop(get_librarian_user)


@pytest.fixture(scope="function")
def authorized_admin(client, session):
    admin = User(
        email="admin@example.com",
        hashed_password="some_hashed_password",
        name="Admin",
        surname="Admin",
        avatar_link="https://example.com/avatar.jpg",
        access_level=2,
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    app.dependency_overrides[get_admin_user] = lambda: admin
    yield client
    app.dependency_overrides.pop(get_admin_user)
