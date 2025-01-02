import pytest
from sqlalchemy.exc import IntegrityError
from app.models.book import Book
from app.models.author import Author


def test_create_book(session):
    new_book = Book(
        title="The Great Adventure",
        description="An epic journey across the world.",
        year_of_publication=2021,
        isbn="1234567890123",
    )
    session.add(new_book)
    session.commit()

    retrieved_book = session.query(Book).filter_by(title="The Great Adventure").first()
    assert retrieved_book is not None
    assert retrieved_book.title == "The Great Adventure"
    assert retrieved_book.description == "An epic journey across the world."
    assert retrieved_book.year_of_publication == 2021
    assert retrieved_book.isbn == "1234567890123"


def test_book_authors_relationship(session):
    new_author = Author(name="Alice", surname="Johnson")
    new_book = Book(
        title="Mystery Novel",
        description="A thrilling mystery.",
        year_of_publication=2022,
        isbn="9876543210987",
    )
    new_book.authors.append(new_author)
    session.add(new_book)
    session.commit()

    retrieved_book = session.query(Book).filter_by(title="Mystery Novel").first()
    assert retrieved_book is not None
    assert len(retrieved_book.authors) == 1
    assert retrieved_book.authors[0].name == "Alice"
    assert retrieved_book.authors[0].surname == "Johnson"


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
