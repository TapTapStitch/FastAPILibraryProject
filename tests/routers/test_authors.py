import pytest
from fastapi import status


valid_author_data = {"name": "John", "surname": "Doe", "year_of_birth": "1990"}


@pytest.fixture
def create_sample_author(client):
    response = client.post("/authors/", json=valid_author_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_sample_book(client):
    book_data = {
        "title": "Sample Book",
        "description": "Sample description",
        "year_of_publication": 2023,
        "isbn": "1234567890123",
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def associate_author_and_book(client, create_sample_author, create_sample_book):
    author_id = create_sample_author["id"]
    book_id = create_sample_book["id"]
    response = client.post(f"/authors/{author_id}/books/{book_id}")
    assert response.status_code == status.HTTP_201_CREATED
    return {"author_id": author_id, "book_id": book_id}


# Test for fetching all authors
def test_get_authors(client):
    response = client.get("/authors/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# Test for fetching an author by ID
def test_get_author_by_id(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == author_id


# Test for attempting to fetch a non-existent author
def test_get_nonexistent_author(client):
    response = client.get("/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for creating a new author
def test_create_author(client):
    response = client.post("/authors/", json=valid_author_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["name"] == valid_author_data["name"]


# Test for creating an author with missing data
def test_create_author_with_missing_data(client):
    invalid_author_data = valid_author_data.copy()
    invalid_author_data["year_of_birth"] = None  # Missing year_of_birth
    response = client.post("/authors/", json=invalid_author_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "int_type",
                "loc": ["body", "year_of_birth"],
                "msg": "Input should be a valid integer",
                "input": None,
            }
        ]
    }


# Test for updating an author
def test_update_author(client, create_sample_author):
    author_id = create_sample_author["id"]
    updated_data = {
        "name": "Updated Name",
        "surname": "Updated Surname",
        "year_of_birth": "1985",
    }
    response = client.patch(f"/authors/{author_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == updated_data["name"]


# Test for updating a non-existent author
def test_update_nonexistent_author(client):
    updated_data = {"name": "Updated Name"}
    response = client.patch("/authors/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for deleting an author
def test_delete_author(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the author is really deleted
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for attempting to delete a non-existent author
def test_delete_nonexistent_author(client):
    response = client.delete("/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for getting books of an author
def test_get_books_of_author(client, associate_author_and_book):
    author_id = associate_author_and_book["author_id"]
    response = client.get(f"/authors/{author_id}/books")
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]
    assert isinstance(books, list)
    assert len(books) > 0
    assert books[0]["title"] == "Sample Book"


# Test for getting books of a non-existent author
def test_get_books_of_nonexistent_author(client):
    response = client.get("/authors/999999/books")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for creating an author-book association
def test_create_author_book_association(
    client, create_sample_author, create_sample_book
):
    author_id = create_sample_author["id"]
    book_id = create_sample_book["id"]
    response = client.post(f"/authors/{author_id}/books/{book_id}")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the association exists
    response = client.get(f"/authors/{author_id}/books")
    books = response.json()["items"]
    assert any(book["id"] == book_id for book in books)


# Test for creating a duplicate author-book association
def test_create_duplicate_author_book_association(client, associate_author_and_book):
    author_id = associate_author_and_book["author_id"]
    book_id = associate_author_and_book["book_id"]
    response = client.post(f"/authors/{author_id}/books/{book_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Association already exists"}


# Test for creating an association with a non-existent author
def test_create_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.post(f"/authors/999999/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for creating an association with a non-existent book
def test_create_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.post(f"/authors/{author_id}/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for deleting an author-book association
def test_delete_author_book_association(client, associate_author_and_book):
    author_id = associate_author_and_book["author_id"]
    book_id = associate_author_and_book["book_id"]
    response = client.delete(f"/authors/{author_id}/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the association is removed
    response = client.get(f"/authors/{author_id}/books")
    books = response.json()["items"]
    assert not any(book["id"] == book_id for book in books)


# Test for deleting a non-existent author-book association
def test_delete_nonexistent_author_book_association(
    client, create_sample_author, create_sample_book
):
    author_id = create_sample_author["id"]
    book_id = create_sample_book["id"]
    response = client.delete(f"/authors/{author_id}/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Association not found"}


# Test for deleting an association with a non-existent author
def test_delete_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/authors/999999/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for deleting an association with a non-existent book
def test_delete_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.delete(f"/authors/{author_id}/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}
