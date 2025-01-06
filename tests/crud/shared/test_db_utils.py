import pytest
from app.models.book import Book
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_unique,
    ensure_association_does_not_exist,
    fetch_association,
)


def test_fetch_by_id(session):
    book = Book(
        title="Test Book",
        description="Test Description",
        year_of_publication=2023,
        isbn="1234567890",
    )
    session.add(book)
    session.commit()

    fetched_book = fetch_by_id(session, Book, book.id, "Book not found")
    assert fetched_book.id == book.id
    assert fetched_book.title == book.title

    with pytest.raises(Exception) as exc_info:
        fetch_by_id(session, Book, 999, "Book not found")
    assert exc_info.value.status_code == 404
    assert "Book not found" in str(exc_info.value)


def test_ensure_unique(session):
    book = Book(
        title="Unique Book",
        description="Description",
        year_of_publication=2023,
        isbn="9876543210",
    )
    session.add(book)
    session.commit()

    with pytest.raises(Exception) as exc_info:
        ensure_unique(session, Book, "isbn", "9876543210", "ISBN must be unique")
    assert exc_info.value.status_code == 400
    assert "ISBN must be unique" in str(exc_info.value)

    # Ensure no exception for unique value
    ensure_unique(session, Book, "isbn", "1234567890", "ISBN must be unique")


def test_ensure_association_does_not_exist(session):
    book = Book(
        title="Test Book",
        description="Description",
        year_of_publication=2023,
        isbn="1234567890",
    )
    session.add(book)
    session.commit()

    with pytest.raises(Exception) as exc_info:
        ensure_association_does_not_exist(session, Book, id=book.id)
    assert exc_info.value.status_code == 400
    assert "Association already exists" in str(exc_info.value)

    # Ensure no exception for non-existing association
    ensure_association_does_not_exist(session, Book, id=999)


def test_fetch_association(session):
    book = Book(
        title="Test Book",
        description="Description",
        year_of_publication=2023,
        isbn="1234567890",
    )
    session.add(book)
    session.commit()

    fetched_book = fetch_association(session, Book, "Book not found", id=book.id)
    assert fetched_book.id == book.id

    with pytest.raises(Exception) as exc_info:
        fetch_association(session, Book, "Book not found", id=999)
    assert exc_info.value.status_code == 404
    assert "Book not found" in str(exc_info.value)
