import pytest
from pydantic import ValidationError
from app.schemas.token import Token


def test_token_creation():
    token = Token(access_token="abc123", token_type="bearer")
    assert token.access_token == "abc123"
    assert token.token_type == "bearer"


def test_token_missing_fields():
    with pytest.raises(ValidationError):
        Token(access_token="abc123")  # Missing token_type

    with pytest.raises(ValidationError):
        Token(token_type="bearer")  # Missing access_token


def test_token_invalid_types():
    with pytest.raises(ValidationError):
        Token(access_token=123, token_type="bearer")  # access_token should be a str

    with pytest.raises(ValidationError):
        Token(access_token="abc123", token_type=456)  # token_type should be a str
