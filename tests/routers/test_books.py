import pytest
from fastapi import status


valid_book_data = {
    "title": "Sample Book",
    "description": "A great book",
    "year_of_publication": 2025,
    "isbn": "1234567890123",
}


@pytest.fixture
def create_sample_book(client):
    response = client.post("/books/", json=valid_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_sample_author(client):
    author_data = {
        "name": "Jane",
        "surname": "Doe",
        "year_of_birth": 1980,
    }
    response = client.post("/authors/", json=author_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def associate_book_and_author(client, create_sample_book, create_sample_author):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.post(f"/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_201_CREATED
    return {"book_id": book_id, "author_id": author_id}


# Test for fetching all books
def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# Test for fetching a book by ID
def test_get_book_by_id(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == book_id


# Test for attempting to fetch a non-existent book
def test_get_nonexistent_book(client):
    response = client.get("/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating a new book
def test_create_book(client):
    response = client.post("/books/", json=valid_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["title"] == valid_book_data["title"]


# Test for creating a book with duplicate ISBN
def test_create_book_with_duplicate_isbn(client, create_sample_book):
    duplicate_isbn_data = valid_book_data.copy()
    duplicate_isbn_data["isbn"] = create_sample_book["isbn"]  # Use the same ISBN
    response = client.post("/books/", json=duplicate_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# Test for updating a book
def test_update_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    updated_data = {"title": "Updated Title", "isbn": "1234567890123"}
    response = client.patch(f"/books/{book_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == updated_data["title"]


# Test for updating a non-existent book
def test_update_nonexistent_book(client):
    updated_data = {"title": "Updated Title"}
    response = client.patch("/books/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for updating a book with invalid ISBN
def test_update_book_with_invalid_isbn(client, create_sample_book):
    another_book = valid_book_data.copy()
    another_book["isbn"] = "1234567890124"
    client.post("/books/", json=another_book)
    book_id = create_sample_book["id"]
    invalid_isbn_data = {"isbn": "1234567890124"}
    response = client.patch(f"/books/{book_id}", json=invalid_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# Test for deleting a book
def test_delete_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the book is really deleted
    response = client.get(f"/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for attempting to delete a non-existent book
def test_delete_nonexistent_book(client):
    response = client.delete("/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for getting authors of a book
def test_get_authors_of_book(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    response = client.get(f"/books/{book_id}/authors")
    assert response.status_code == status.HTTP_200_OK
    authors = response.json()["items"]
    assert isinstance(authors, list)
    assert len(authors) > 0
    assert authors[0]["name"] == "Jane"


# Test for getting authors of a non-existent book
def test_get_authors_of_nonexistent_book(client):
    response = client.get("/books/999999/authors")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating a book-author association
def test_create_book_author_association(
    client, create_sample_book, create_sample_author
):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.post(f"/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the association exists
    response = client.get(f"/books/{book_id}/authors")
    authors = response.json()["items"]
    assert any(author["id"] == author_id for author in authors)


# Test for creating a duplicate book-author association
def test_create_duplicate_book_author_association(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    author_id = associate_book_and_author["author_id"]
    response = client.post(f"/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Association already exists"}


# Test for creating an association with a non-existent book
def test_create_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.post(f"/books/999999/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating an association with a non-existent author
def test_create_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.post(f"/books/{book_id}/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for deleting a book-author association
def test_delete_book_author_association(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    author_id = associate_book_and_author["author_id"]
    response = client.delete(f"/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the association is removed
    response = client.get(f"/books/{book_id}/authors")
    authors = response.json()["items"]
    assert not any(author["id"] == author_id for author in authors)


# Test for deleting a non-existent book-author association
def test_delete_nonexistent_book_author_association(
    client, create_sample_book, create_sample_author
):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.delete(f"/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Association not found"}


# Test for deleting an association with a non-existent book
def test_delete_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.delete(f"/books/999999/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for deleting an association with a non-existent author
def test_delete_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/books/{book_id}/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}
