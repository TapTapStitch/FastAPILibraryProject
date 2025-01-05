import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.book import Book


def test_create_book(session):
    new_book = Book(
        title="The Great Adventure",
        description="An epic journey across the world.",
        year_of_publication=2021,
        isbn="1234567890123",
    )
    session.add(new_book)
    session.commit()

    stmt = select(Book).where(Book.title == "The Great Adventure")
    retrieved_book = session.execute(stmt).scalar_one_or_none()
    assert retrieved_book is not None
    assert retrieved_book.title == "The Great Adventure"
    assert retrieved_book.description == "An epic journey across the world."
    assert retrieved_book.year_of_publication == 2021
    assert retrieved_book.isbn == "1234567890123"


def test_unique_isbn_constraint(session):
    book1 = Book(
        title="First Book",
        description="Description of the first book.",
        year_of_publication=2020,
        isbn="unique-isbn-123",
    )
    session.add(book1)
    session.commit()

    book2 = Book(
        title="Second Book",
        description="Description of the second book.",
        year_of_publication=2021,
        isbn="unique-isbn-123",
    )
    session.add(book2)
    with pytest.raises(IntegrityError):
        session.commit()
