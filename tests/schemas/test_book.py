from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.api.v1.book import (
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
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
        )


def test_create_book_schema():
    # Valid data
    book_data = CreateBookSchema(
        title="Python Basics",
        description="",
        year_of_publication=2020,
        isbn="1234567890123",
    )
    assert book_data.title == "Python Basics"

    # Missing required field
    with pytest.raises(ValidationError):
        CreateBookSchema(
            description="A book about Python programming.",
            year_of_publication=2020,
            isbn="1234567890123",
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
