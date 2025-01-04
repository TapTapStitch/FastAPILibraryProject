import pytest
from fastapi import HTTPException
from app.crud.books import BooksCrud
from app.schemas.book import CreateBookSchema, UpdateBookSchema
from app.schemas.pagination import PaginationParams
from app.models.book import Book
from app.models.author import Author
from app.models.book_author import BookAuthor


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


@pytest.fixture
def sample_author(session):
    author = Author(name="Sample Author")
    session.add(author)
    session.commit()
    return author


@pytest.fixture
def book_author_association(session, sample_book, sample_author):
    association = BookAuthor(book_id=sample_book.id, author_id=sample_author.id)
    session.add(association)
    session.commit()
    return association


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


# Positive case: Get authors of a book
def test_get_authors_of_book(book_crud, sample_book, book_author_association):
    pagination = PaginationParams(page=1, size=10)
    authors = book_crud.get_authors_of_book(sample_book.id, pagination)
    assert len(authors.items) == 1
    assert authors.items[0].name == "Sample Author"


# Negative case: Get authors of a non-existent book
def test_get_authors_of_non_existent_book(book_crud):
    pagination = PaginationParams(page=1, size=10)
    with pytest.raises(HTTPException) as excinfo:
        book_crud.get_authors_of_book(
            999, pagination
        )  # Assuming book ID 999 doesn't exist
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Positive case: Create book-author association
def test_create_book_author_association(book_crud, sample_book, sample_author):
    book_crud.create_book_author_association(sample_book.id, sample_author.id)
    association = (
        book_crud.db.query(BookAuthor)
        .filter_by(book_id=sample_book.id, author_id=sample_author.id)
        .first()
    )
    assert association is not None


# Negative case: Create duplicate book-author association
def test_create_duplicate_book_author_association(book_crud, book_author_association):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.create_book_author_association(
            book_author_association.book_id, book_author_association.author_id
        )
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Association already exists"


# Negative case: Create association for non-existent book
def test_create_association_non_existent_book(book_crud, sample_author):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.create_book_author_association(
            999, sample_author.id
        )  # Non-existent book
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Negative case: Create association for non-existent author
def test_create_association_non_existent_author(book_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.create_book_author_association(
            sample_book.id, 999
        )  # Non-existent author
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"


# Positive case: Remove book-author association
def test_remove_book_author_association(book_crud, book_author_association):
    book_crud.remove_book_author_association(
        book_author_association.book_id, book_author_association.author_id
    )
    association = (
        book_crud.db.query(BookAuthor)
        .filter_by(
            book_id=book_author_association.book_id,
            author_id=book_author_association.author_id,
        )
        .first()
    )
    assert association is None


# Negative case: Remove non-existent book-author association
def test_remove_non_existent_book_author_association(
    book_crud, sample_book, sample_author
):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.remove_book_author_association(sample_book.id, sample_author.id)
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Association not found"


# Negative case: Remove association for non-existent book
def test_remove_association_non_existent_book(book_crud, sample_author):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.remove_book_author_association(
            999, sample_author.id
        )  # Non-existent book
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Book not found"


# Negative case: Remove association for non-existent author
def test_remove_association_non_existent_author(book_crud, sample_book):
    with pytest.raises(HTTPException) as excinfo:
        book_crud.remove_book_author_association(
            sample_book.id, 999
        )  # Non-existent author
    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Author not found"
