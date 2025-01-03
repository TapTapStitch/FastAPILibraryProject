import pytest
from fastapi import HTTPException
from app.crud.books import BooksCrud
from app.schemas.book import CreateBookSchema, UpdateBookSchema
from app.models.book import Book


@pytest.fixture()
def book_crud(session):
    return BooksCrud(db=session)


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


# Positive case: Create a new book
def test_create_book(book_crud):
    book_data = CreateBookSchema(
        title="New Book",
        description="A new book description",
        year_of_publication=2023,
        isbn="0987654321098",  # Valid 13-digit ISBN
    )
    book = book_crud.create_book(book_data)
    assert book.title == "New Book"
    assert book.isbn == "0987654321098"


# Negative case: Create a book with a duplicate ISBN
def test_create_book_with_duplicate_isbn(book_crud, sample_book):
    book_data = CreateBookSchema(
        title="Another Book",
        description="Another book description",
        year_of_publication=2023,
        isbn=sample_book.isbn,  # Duplicate ISBN
    )
    with pytest.raises(HTTPException) as excinfo:
        book_crud.create_book(book_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "ISBN must be unique"


# Positive case: Retrieve a book by ID
def test_get_book_by_id(book_crud, sample_book):
    book = book_crud.get_book_by_id(sample_book.id)
    assert book.title == "Sample Book"


# Negative case: Retrieve a book with non-existent ID
def test_get_book_by_id_not_found(book_crud):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.get_book_by_id(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Positive case: Update a book's title
def test_update_book(book_crud, sample_book):
    update_data = UpdateBookSchema(title="Updated Book Title")
    updated_book = book_crud.update_book(sample_book.id, update_data)
    assert updated_book.title == "Updated Book Title"


# Negative case: Update a book with a duplicate ISBN
def test_update_book_with_duplicate_isbn(book_crud, sample_book, session):
    # Create another book to have a duplicate ISBN scenario
    another_book = Book(
        title="Another Book",
        description="Another description",
        year_of_publication=2023,
        isbn="2222222222222",  # Valid 13-digit ISBN
    )
    session.add(another_book)
    session.commit()

    update_data = UpdateBookSchema(isbn="2222222222222")  # ISBN of another_book
    with pytest.raises(HTTPException) as excinfo:
        book_crud.update_book(sample_book.id, update_data)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "ISBN must be unique"


# Positive case: Remove a book
def test_remove_book(book_crud, sample_book):
    book_crud.remove_book(sample_book.id)
    with pytest.raises(HTTPException) as excinfo:
        book_crud.get_book_by_id(sample_book.id)
    assert excinfo.value.status_code == 404


# Negative case: Remove a book with non-existent ID
def test_remove_book_not_found(book_crud):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.remove_book(999)  # Assuming this ID doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"
