from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.book import (
    AuthorInBookSchema,
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
)


def test_author_in_book_schema():
    # Valid data
    author = AuthorInBookSchema(
        id=1,
        name="John",
        surname="Doe",
        year_of_birth=1980,
        biography="Biography of John Doe.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert author.name == "John"

    # Invalid data
    with pytest.raises(ValidationError):
        AuthorInBookSchema(
            id=1,
            name="John",
            surname="Doe",
            year_of_birth=999,  # Invalid year
            biography="Biography of John Doe.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


def test_book_schema():
    # Valid data
    book = BookSchema(
        id=1,
        title="Python Basics",
        description="A book about Python programming.",
        year_of_publication=2020,
        isbn="1234567890123",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        authors=[
            {
                "id": 1,
                "name": "John",
                "surname": "Doe",
                "year_of_birth": 1980,
                "biography": "Biography of John Doe.",
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
        ],
    )
    assert book.title == "Python Basics"

    # Invalid ISBN
    with pytest.raises(ValidationError):
        BookSchema(
            id=1,
            title="Python Basics",
            description="A book about Python programming.",
            year_of_publication=2020,
            isbn="123",  # Invalid ISBN
            created_at=datetime.now(),
            updated_at=datetime.now(),
            authors=[],
        )


def test_create_book_schema():
    # Valid data
    book_data = CreateBookSchema(
        title="Python Basics",
        description="",
        year_of_publication=2020,
        isbn="1234567890123",
        authors=[1, 2],
    )
    assert book_data.title == "Python Basics"

    # Missing required field
    with pytest.raises(ValidationError):
        CreateBookSchema(
            description="A book about Python programming.",
            year_of_publication=2020,
            isbn="1234567890123",
            authors=[1, 2],
        )


def test_update_book_schema():
    # Valid data
    book_data = UpdateBookSchema(
        title="Advanced Python",
    )
    assert book_data.title == "Advanced Python"

    # Invalid ISBN
    with pytest.raises(ValidationError):
        UpdateBookSchema(title="Advanced Python", isbn="123")  # Invalid ISBN
