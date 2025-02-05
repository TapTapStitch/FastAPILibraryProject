from pydantic import ValidationError
from datetime import datetime
import pytest
from app.schemas.api.v1.user import (
    UserSchema,
    SignUpSchema,
    UpdateUserSchema,
    SignInSchema,
    validate_password,
)

# Sample data for testing
valid_email = "test@example.com"
invalid_email = "invalid-email"
valid_password = "Valid123"
invalid_password = "short"
current_time = datetime.now()


def test_user_schema_valid():
    user = UserSchema(
        id=1,
        email=valid_email,
        name="John",
        surname="Doe",
        created_at=current_time,
        updated_at=current_time,
    )
    assert user.id == 1
    assert user.email == valid_email
    assert user.name == "John"
    assert user.surname == "Doe"
    assert user.created_at == current_time
    assert user.updated_at == current_time


def test_user_schema_invalid_email():
    with pytest.raises(ValidationError):
        UserSchema(
            id=1,
            email=invalid_email,
            name="John",
            surname="Doe",
            created_at=current_time,
            updated_at=current_time,
        )


def test_signup_schema_valid():
    signup = SignUpSchema(
        name="John",
        surname="Doe",
        email=valid_email,
        password=valid_password,
    )
    assert signup.name == "John"
    assert signup.surname == "Doe"
    assert signup.email == valid_email
    assert signup.password == valid_password


def test_signup_schema_invalid_password():
    with pytest.raises(ValidationError):
        SignUpSchema(
            name="John",
            surname="Doe",
            email=valid_email,
            password=invalid_password,
        )


def test_update_user_schema_valid():
    update = UpdateUserSchema(
        name="Jane",
        email="jane@example.com",
    )
    assert update.name == "Jane"
    assert update.email == "jane@example.com"
    assert update.surname is None
    assert update.password is None


def test_signin_schema_valid():
    signin = SignInSchema(
        email=valid_email,
        password=valid_password,
    )
    assert signin.email == valid_email
    assert signin.password == valid_password


def test_signin_schema_invalid_email():
    with pytest.raises(ValidationError):
        SignInSchema(
            email=invalid_email,
            password=valid_password,
        )


def test_validate_password():
    assert validate_password("Valid123") == "Valid123"
    with pytest.raises(ValueError):
        validate_password("short")
    with pytest.raises(ValueError):
        validate_password("alllowercase1")
    with pytest.raises(ValueError):
        validate_password("ALLUPPERCASE1")
    with pytest.raises(ValueError):
        validate_password("NoDigitsHere")
