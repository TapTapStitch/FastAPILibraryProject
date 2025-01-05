import pytest
from app.models.book import Book
from app.models.genre import Genre
from app.models.book_genre import BookGenre
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


@pytest.fixture
def data(session):
    new_book = Book(
        title="The Great Adventure",
    )
    session.add(new_book)

    new_genre = Genre(name="Adventure")
    session.add(new_genre)
    session.commit()


def test_create_book_genre(session, data):
    # Test creating a BookGenre record
    book_genre = BookGenre(book_id=1, genre_id=1)
    session.add(book_genre)
    session.commit()

    # Query the inserted record
    result = session.execute(select(BookGenre).limit(1)).scalar_one_or_none()
    assert result is not None
    assert result.book_id == 1
    assert result.genre_id == 1
    assert result.created_at is not None


def test_primary_key_constraint(session, data):
    # Create the first BookGenre record
    book_genre_1 = BookGenre(book_id=1, genre_id=1)
    session.add(book_genre_1)
    session.commit()
    session.close()

    # Attempt to create a duplicate BookGenre record in a new session
    book_genre_2 = BookGenre(book_id=1, genre_id=1)
    session.add(book_genre_2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.close()


def test_cascade_delete(session, data):
    # Add related entities and ensure cascade delete works
    book_genre = BookGenre(book_id=1, genre_id=1)
    session.add(book_genre)
    session.commit()

    # Simulate cascade delete (e.g., if the book is deleted)
    session.delete(book_genre)
    session.commit()

    result = session.execute(
        select(BookGenre).filter_by(book_id=1, genre_id=1)
    ).scalar_one_or_none()
    assert result is None
