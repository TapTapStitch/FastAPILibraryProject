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


# 1. Test for fetching all books
def test_get_books(client):
    response = client.get("/books/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# 2. Test for fetching a book by ID
def test_get_book_by_id(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.get(f"/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == book_id


# 3. Test for attempting to fetch a non-existent book
def test_get_nonexistent_book(client):
    response = client.get("/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# 4. Test for creating a new book
def test_create_book(client):
    response = client.post("/books/", json=valid_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["title"] == valid_book_data["title"]


# 5. Test for creating a book with duplicate ISBN
def test_create_book_with_duplicate_isbn(client, create_sample_book):
    duplicate_isbn_data = valid_book_data.copy()
    duplicate_isbn_data["isbn"] = create_sample_book["isbn"]  # Use the same ISBN
    response = client.post("/books/", json=duplicate_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# 6. Test for updating a book
def test_update_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    updated_data = {"title": "Updated Title", "isbn": "1234567890123"}
    response = client.patch(f"/books/{book_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == updated_data["title"]


# 7. Test for updating a non-existent book
def test_update_nonexistent_book(client):
    updated_data = {"title": "Updated Title"}
    response = client.patch("/books/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# 8. Test for updating a book with invalid ISBN
def test_update_book_with_invalid_isbn(client, create_sample_book):
    another_book = valid_book_data.copy()
    another_book["isbn"] = "1234567890124"
    client.post("/books/", json=another_book)
    book_id = create_sample_book["id"]
    invalid_isbn_data = {"isbn": "1234567890124"}
    response = client.patch(f"/books/{book_id}", json=invalid_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# 9. Test for deleting a book
def test_delete_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the book is really deleted
    response = client.get(f"/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# 10. Test for attempting to delete a non-existent book
def test_delete_nonexistent_book(client):
    response = client.delete("/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}
