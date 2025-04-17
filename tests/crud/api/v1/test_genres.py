import pytest
from fastapi import HTTPException
from app.crud.api.v1.genres import GenresCrud
from app.schemas.api.v1.genre import CreateGenreSchema, UpdateGenreSchema
from app.schemas.api.v1.book import BookSortingSchema
from app.schemas.pagination import PaginationParams
from app.models.genre import Genre
from app.models.book import Book
from app.models.book_genre import BookGenre


@pytest.fixture
def genre_crud(session):
    return GenresCrud(db=session)


@pytest.fixture
def sample_genre(session):
    genre = Genre(name="Sample Genre")
    session.add(genre)
    session.commit()
    return genre


@pytest.fixture
def sample_book(session):
    book = Book(
        title="Sample Book",
        description="A sample book description",
        year_of_publication=2023,
        isbn="1234567890123",  # 13-digit ISBN
    )
    session.add(book)
    session.commit()
    return book


@pytest.fixture
def genre_book_association(session, sample_genre, sample_book):
    association = BookGenre(book_id=sample_book.id, genre_id=sample_genre.id)
    session.add(association)
    session.commit()
    return association


# Positive case: Create a new genre
def test_create_genre(genre_crud):
    genre_data = CreateGenreSchema(name="New Genre")
    genre = genre_crud.create_genre(genre_data)
    assert genre.name == "New Genre"


# Positive case: Retrieve a genre by ID
def test_get_genre_by_id(genre_crud, sample_genre):
    genre = genre_crud.get_genre_by_id(sample_genre.id)
    assert genre.name == "Sample Genre"


# Negative case: Retrieve a genre with a non-existent ID
def test_get_genre_by_id_not_found(genre_crud):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.get_genre_by_id(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Genre not found"


# Positive case: Update a genre's name
def test_update_genre(genre_crud, sample_genre):
    update_data = UpdateGenreSchema(name="Updated Genre")
    updated_genre = genre_crud.update_genre(sample_genre.id, update_data)
    assert updated_genre.name == "Updated Genre"


# Positive case: Remove a genre
def test_remove_genre(genre_crud, sample_genre):
    genre_crud.remove_genre(sample_genre.id)
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.get_genre_by_id(sample_genre.id)
    assert excinfo.value.status_code == 404


# Negative case: Remove a genre with a non-existent ID
def test_remove_genre_not_found(genre_crud):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.remove_genre(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Genre not found"


# Positive case: Get books of a genre
def test_get_books_of_genre(genre_crud, sample_genre, genre_book_association):
    pagination = PaginationParams(page=1, size=10)
    books = genre_crud.get_books_of_genre(
        sample_genre.id, {}, BookSortingSchema(), pagination
    )
    assert len(books.items) == 1
    assert books.items[0].title == "Sample Book"


# Negative case: Get books of a non-existent genre
def test_get_books_of_non_existent_genre(genre_crud):
    pagination = PaginationParams(page=1, size=10)
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.get_books_of_genre(
            999, {}, BookSortingSchema(), pagination
        )  # Assuming genre ID 999 doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Genre not found"


# Positive case: Create genre-book association
def test_create_genre_book_association(genre_crud, sample_genre, sample_book):
    genre_crud.create_genre_book_association(sample_genre.id, sample_book.id)
    association = (
        genre_crud.db.query(BookGenre)
        .filter_by(genre_id=sample_genre.id, book_id=sample_book.id)
        .first()
    )
    assert association is not None


# Negative case: Create duplicate genre-book association
def test_create_duplicate_genre_book_association(genre_crud, genre_book_association):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.create_genre_book_association(
            genre_book_association.genre_id, genre_book_association.book_id
        )
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Association already exists"


# Negative case: Create association for non-existent genre
def test_create_association_non_existent_genre(genre_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.create_genre_book_association(
            999, sample_book.id  # Non-existent genre
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Genre not found"


# Negative case: Create association for non-existent book
def test_create_association_non_existent_book(genre_crud, sample_genre):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.create_genre_book_association(
            sample_genre.id, 999  # Non-existent book
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Positive case: Remove genre-book association
def test_remove_genre_book_association(genre_crud, genre_book_association):
    genre_crud.remove_genre_book_association(
        genre_book_association.genre_id, genre_book_association.book_id
    )
    association = (
        genre_crud.db.query(BookGenre)
        .filter_by(
            genre_id=genre_book_association.genre_id,
            book_id=genre_book_association.book_id,
        )
        .first()
    )
    assert association is None


# Negative case: Remove non-existent genre-book association
def test_remove_non_existent_genre_book_association(
    genre_crud, sample_genre, sample_book
):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.remove_genre_book_association(sample_genre.id, sample_book.id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Association not found"


# Negative case: Remove association for non-existent genre
def test_remove_association_non_existent_genre(genre_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.remove_genre_book_association(
            999, sample_book.id  # Non-existent genre
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Genre not found"


# Negative case: Remove association for non-existent book
def test_remove_association_non_existent_book(genre_crud, sample_genre):
    with pytest.raises(HTTPException) as excinfo:
        genre_crud.remove_genre_book_association(
            sample_genre.id, 999  # Non-existent book
        )
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"
