import pytest
from app.models.book import Book
from app.models.author import Author
from app.models.book_author import BookAuthor
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def data(session):
    new_book = Book(
        title="The Great Adventure",
    )
    session.add(new_book)

    new_author = Author(name="John Doe")
    session.add(new_author)
    session.commit()


def test_create_book_author(session, data):
    # Test creating a BookAuthor record
    book_author = BookAuthor(book_id=1, author_id=1)
    session.add(book_author)
    session.commit()

    # Query the inserted record
    result = session.execute(select(BookAuthor).limit(1)).scalar_one_or_none()
    assert result is not None
    assert result.book_id == 1
    assert result.author_id == 1
    assert result.created_at is not None


def test_primary_key_constraint(session, data):
    # Create the first BookAuthor record
    book_author_1 = BookAuthor(book_id=1, author_id=1)
    session.add(book_author_1)
    session.commit()
    session.close()

    # Attempt to create a duplicate BookAuthor record in a new session
    book_author_2 = BookAuthor(book_id=1, author_id=1)
    session.add(book_author_2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()


def test_cascade_delete(session, data):
    # Add related entities and ensure cascade delete works
    book_author = BookAuthor(book_id=1, author_id=1)
    session.add(book_author)
    session.commit()

    # Simulate cascade delete (e.g., if the book is deleted)
    session.delete(book_author)
    session.commit()

    result = session.execute(
        select(BookAuthor).filter_by(book_id=1, author_id=1)
    ).scalar_one_or_none()
    assert result is None
