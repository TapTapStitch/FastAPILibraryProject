import pytest
from fastapi import HTTPException
from app.crud.api.v1.authors import AuthorsCrud
from app.schemas.api.v1.author import CreateAuthorSchema, UpdateAuthorSchema
from app.schemas.api.v1.book import BookSortingSchema
from app.schemas.pagination import PaginationParams
from app.models.author import Author
from app.models.book import Book
from app.models.book_author import BookAuthor


@pytest.fixture
def author_crud(session):
    return AuthorsCrud(db=session)


@pytest.fixture
def sample_author(session):
    author = Author(
        name="Sample",
        surname="Author",
        year_of_birth=1970,
        biography="A sample biography",
    )
    session.add(author)
    session.commit()
    return author


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
def author_book_association(session, sample_author, sample_book):
    association = BookAuthor(book_id=sample_book.id, author_id=sample_author.id)
    session.add(association)
    session.commit()
    return association


# Positive case: Create a new author
def test_create_author(author_crud):
    author_data = CreateAuthorSchema(
        name="New",
        surname="Author",
        year_of_birth=1980,
        biography="A new author biography",
    )
    author = author_crud.create_author(author_data)
    assert author.name == "New"
    assert author.surname == "Author"


# Positive case: Retrieve an author by ID
def test_get_author_by_id(author_crud, sample_author):
    author = author_crud.get_author_by_id(sample_author.id)
    assert author.name == "Sample"
    assert author.surname == "Author"


# Negative case: Retrieve an author with a non-existent ID
def test_get_author_by_id_not_found(author_crud):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.get_author_by_id(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Positive case: Update an author's biography
def test_update_author(author_crud, sample_author):
    update_data = UpdateAuthorSchema(biography="Updated biography")
    updated_author = author_crud.update_author(sample_author.id, update_data)
    assert updated_author.biography == "Updated biography"


# Positive case: Remove an author
def test_remove_author(author_crud, sample_author):
    author_crud.remove_author(sample_author.id)
    with pytest.raises(HTTPException) as excinfo:
        author_crud.get_author_by_id(sample_author.id)
    assert excinfo.value.status_code == 404


# Negative case: Remove an author with a non-existent ID
def test_remove_author_not_found(author_crud):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.remove_author(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Positive case: Get books of an author
def test_get_books_of_author(author_crud, sample_author, author_book_association):
    pagination = PaginationParams(page=1, size=10)
    books = author_crud.get_books_of_author(
        sample_author.id, pagination, BookSortingSchema()
    )
    assert len(books.items) == 1
    assert books.items[0].title == "Sample Book"


# Negative case: Get books of a non-existent author
def test_get_books_of_non_existent_author(author_crud):
    pagination = PaginationParams(page=1, size=10)
    with pytest.raises(HTTPException) as excinfo:
        author_crud.get_books_of_author(
            999, pagination, BookSortingSchema()
        )  # Assuming author ID 999 doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Positive case: Create author-book association
def test_create_author_book_association(author_crud, sample_author, sample_book):
    author_crud.create_author_book_association(sample_author.id, sample_book.id)
    association = (
        author_crud.db.query(BookAuthor)
        .filter_by(author_id=sample_author.id, book_id=sample_book.id)
        .first()
    )
    assert association is not None


# Negative case: Create duplicate author-book association
def test_create_duplicate_author_book_association(author_crud, author_book_association):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.create_author_book_association(
            author_book_association.author_id, author_book_association.book_id
        )
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Association already exists"


# Negative case: Create association for non-existent author
def test_create_association_non_existent_author(author_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.create_author_book_association(
            999, sample_book.id
        )  # Non-existent author
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Negative case: Create association for non-existent book
def test_create_association_non_existent_book(author_crud, sample_author):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.create_author_book_association(
            sample_author.id, 999
        )  # Non-existent book
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Positive case: Remove author-book association
def test_remove_author_book_association(author_crud, author_book_association):
    author_crud.remove_author_book_association(
        author_book_association.author_id, author_book_association.book_id
    )
    association = (
        author_crud.db.query(BookAuthor)
        .filter_by(
            author_id=author_book_association.author_id,
            book_id=author_book_association.book_id,
        )
        .first()
    )
    assert association is None


# Negative case: Remove non-existent author-book association
def test_remove_non_existent_author_book_association(
    author_crud, sample_author, sample_book
):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.remove_author_book_association(sample_author.id, sample_book.id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Association not found"


# Negative case: Remove association for non-existent author
def test_remove_association_non_existent_author(author_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.remove_author_book_association(
            999, sample_book.id
        )  # Non-existent author
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Negative case: Remove association for non-existent book
def test_remove_association_non_existent_book(author_crud, sample_author):
    with pytest.raises(HTTPException) as excinfo:
        author_crud.remove_author_book_association(
            sample_author.id, 999
        )  # Non-existent book
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"
