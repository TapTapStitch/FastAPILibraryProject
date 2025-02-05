from sqlalchemy import select
from app.models.user import User


def test_create_user(session):
    new_user = User(
        email="test@example.com",
        hashed_password="hashedpassword123",
        name="John",
        surname="Doe",
        avatar_link="https://example.com/avatar.jpg",
        access_level=1,
    )
    session.add(new_user)
    session.commit()

    stmt = select(User).where(User.email == "test@example.com")
    result = session.execute(stmt).scalar_one_or_none()

    assert result is not None
    assert result.email == "test@example.com"
    assert result.hashed_password == "hashedpassword123"
    assert result.name == "John"
    assert result.surname == "Doe"
    assert result.avatar_link == "https://example.com/avatar.jpg"
    assert result.access_level == 1
    assert result.created_at is not None
    assert result.updated_at is not None
