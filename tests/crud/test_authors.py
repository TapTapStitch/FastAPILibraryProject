import pytest
from fastapi import HTTPException
from app.crud.authors import AuthorsCrud
from app.schemas.author import CreateAuthorSchema, UpdateAuthorSchema
from app.models.author import Author
from app.models.book import Book


@pytest.fixture
def author_crud(session):
    return AuthorsCrud(db=session)


@pytest.fixture
def sample_book(session):
    book = Book(
        title="Sample Book",
        description="A sample book description",
        year_of_publication=2023,
        isbn="1234567890123",
    )
    session.add(book)
    session.commit()
    return book


@pytest.fixture
def sample_author(session, sample_book):
    author = Author(
        name="Sample",
        surname="Author",
        year_of_birth=1970,
        biography="A sample biography",
        books=[sample_book],
    )
    session.add(author)
    session.commit()
    return author


# Positive case: Create a new author
def test_create_author(author_crud, sample_book):
    author_data = CreateAuthorSchema(
        name="New",
        surname="Author",
        year_of_birth=1980,
        biography="A new author biography",
        books=[sample_book.id],
    )
    author = author_crud.create_author(author_data)
    assert author.name == "New"
    assert author.surname == "Author"
    assert len(author.books) == 1
    assert author.books[0].title == "Sample Book"


# Negative case: Create an author with a non-existent book
def test_create_author_with_nonexistent_book(author_crud):
    author_data = CreateAuthorSchema(
        name="Another",
        surname="Author",
        year_of_birth=1985,
        biography="Another author biography",
        books=[9999],  # Assuming this book ID doesn't exist
    )
    with pytest.raises(HTTPException) as excinfo:
        author_crud.create_author(author_data)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "One or more books not found"


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


# Negative case: Update an author with a non-existent book
def test_update_author_with_nonexistent_book(author_crud, sample_author):
    update_data = UpdateAuthorSchema(
        books=[9999]  # Assuming this book ID doesn't exist
    )
    with pytest.raises(HTTPException) as excinfo:
        author_crud.update_author(sample_author.id, update_data)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "One or more books not found"


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
