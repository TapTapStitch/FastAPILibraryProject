from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.author import (
    AuthorSchema,
    BookInAuthorSchema,
    CreateAuthorSchema,
    UpdateAuthorSchema,
)


def test_book_in_author_schema():
    # Valid data
    book = BookInAuthorSchema(
        id=1,
        title="Learn Python",
        description="An introductory book about Python.",
        year_of_publication=2020,
        isbn="1234567890123",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert book.title == "Learn Python"

    # Invalid ISBN
    with pytest.raises(ValidationError):
        BookInAuthorSchema(
            id=1,
            title="Learn Python",
            description="An introductory book about Python.",
            year_of_publication=2020,
            isbn="123",  # Invalid ISBN
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


def test_author_schema():
    # Valid data
    author = AuthorSchema(
        id=1,
        name="Jane",
        surname="Doe",
        year_of_birth=1985,
        biography="Biography of Jane Doe.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        books=[
            {
                "id": 1,
                "title": "Learn Python",
                "description": "An introductory book about Python.",
                "year_of_publication": 2020,
                "isbn": "1234567890123",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ],
    )
    assert author.name == "Jane"

    # Invalid year_of_birth
    with pytest.raises(ValidationError):
        AuthorSchema(
            id=1,
            name="Jane",
            surname="Doe",
            year_of_birth=999,  # Invalid year
            biography="Biography of Jane Doe.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            books=[],
        )


def test_create_author_schema():
    # Valid data
    author_data = CreateAuthorSchema(
        name="Jane", surname="Doe", year_of_birth=1985, biography="", books=[1, 2]
    )
    assert author_data.name == "Jane"

    # Missing required field
    with pytest.raises(ValidationError):
        CreateAuthorSchema(
            surname="Doe", year_of_birth=1985, biography="", books=[1, 2]
        )


def test_update_author_schema():
    # Valid data
    author_data = UpdateAuthorSchema(
        name="John",
    )
    assert author_data.name == "John"

    # Invalid year of birth
    with pytest.raises(ValidationError):
        UpdateAuthorSchema(year_of_birth=999)  # Invalid year
