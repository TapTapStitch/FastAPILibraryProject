import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.api.v1.user import SignUpSchema, SignInSchema, UpdateUserSchema
from app.crud.api.v1.users import UsersCrud


@pytest.fixture
def user_crud(session: Session):
    return UsersCrud(db=session)


@pytest.fixture
def sample_user(session: Session, user_crud: UsersCrud):
    user = SignUpSchema(
        email="test@example.com",
        password="ValidPass123",
        name="Test",
        surname="User",
        avatar_link="https://example.com/avatar.jpg",
    )
    user = user_crud.sign_up_user(user)
    return user


# Positive Test: Sign up a new user
def test_sign_up_user(user_crud):
    user_data = SignUpSchema(
        name="New",
        surname="User",
        email="newuser@example.com",
        password="ValidPass123",
        avatar_link="https://example.com/avatar.jpg",
    )
    user = user_crud.sign_up_user(user_data)
    assert user.email == "newuser@example.com"
    assert user.name == "New"
    assert user.surname == "User"


# Negative Test: Sign up with an existing email
def test_sign_up_user_existing_email(user_crud, sample_user):
    user_data = SignUpSchema(
        name="Another",
        surname="User",
        email="test@example.com",  # Email already exists
        password="ValidPass123",
        avatar_link="https://example.com/avatar.jpg",
    )
    with pytest.raises(HTTPException) as excinfo:
        user_crud.sign_up_user(user_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Email already in use"


# Positive Test: Sign in with correct credentials
def test_sign_in_user(user_crud, sample_user):
    user_data = SignInSchema(
        email="test@example.com",
        password="ValidPass123",  # Assuming this matches the hashed password
    )
    user = user_crud.sign_in_user(user_data)
    assert user.email == "test@example.com"


# Negative Test: Sign in with incorrect password
def test_sign_in_user_invalid_password(user_crud, sample_user):
    user_data = SignInSchema(email="test@example.com", password="InvalidPass123")
    with pytest.raises(HTTPException) as excinfo:
        user_crud.sign_in_user(user_data)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Invalid password"


# Negative Test: Sign in with non-existent email
def test_sign_in_user_non_existent_email(user_crud):
    user_data = SignInSchema(email="nonexistent@example.com", password="ValidPass123")
    with pytest.raises(HTTPException) as excinfo:
        user_crud.sign_in_user(user_data)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "User not found"


# Positive Test: Update user details
def test_update_user(user_crud, sample_user):
    update_data = UpdateUserSchema(
        name="Updated", surname="User", email="updated@example.com"
    )
    updated_user = user_crud.update_user(sample_user, update_data)
    assert updated_user.name == "Updated"
    assert updated_user.surname == "User"
    assert updated_user.email == "updated@example.com"


# Negative Test: Update user with existing email
def test_update_user_existing_email(user_crud, sample_user, session: Session):
    # Create another user with a different email
    another_user = User(
        email="another@example.com",
        hashed_password="$2b$12$KIXTOzQF5Y8G1Z1Z1Z1Z1u",
        name="Another",
        surname="User",
        avatar_link="https://example.com/avatar.jpg",
    )
    session.add(another_user)
    session.commit()

    update_data = UpdateUserSchema(
        email="another@example.com"  # Email already in use by another_user
    )
    with pytest.raises(HTTPException) as excinfo:
        user_crud.update_user(sample_user, update_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Email already in use"


# Positive Test: Remove user
def test_remove_user(user_crud, sample_user):
    user_crud.remove_user(sample_user)
    # Attempt to fetch the user should raise an exception or return None
    with pytest.raises(HTTPException) as excinfo:
        user_crud.sign_in_user(
            SignInSchema(email="test@example.com", password="ValidPass123")
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "User not found"


# Negative Test: Remove non-existent user
def test_remove_non_existent_user(user_crud, session: Session):
    non_existent_user = User(
        id=999,  # Assuming this ID doesn't exist
        email="nonexistent@example.com",
        hashed_password="$2b$12$KIXTOzQF5Y8G1Z1Z1Z1Z1u",
        name="Non",
        surname="Existent",
        avatar_link="https://example.com/avatar.jpg",
    )
    with pytest.raises(Exception):
        user_crud.remove_user(non_existent_user)
