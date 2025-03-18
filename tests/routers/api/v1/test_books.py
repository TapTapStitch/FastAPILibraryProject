import pytest
from fastapi import status


valid_book_data = {
    "title": "Sample Book",
    "description": "A great book",
    "year_of_publication": 2025,
    "isbn": "1234567890123",
    "series": "Sample Series",
    "file_link": "https://example.com/sample.pdf",
    "edition": "First",
}


@pytest.fixture
def create_sample_book(client):
    response = client.post("/api/v1/books/", json=valid_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def create_sample_author(client):
    author_data = {
        "name": "Jane",
        "surname": "Doe",
        "year_of_birth": 1980,
    }
    response = client.post("/api/v1/authors/", json=author_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def associate_book_and_author(client, create_sample_book, create_sample_author):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.post(f"/api/v1/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_201_CREATED
    return {"book_id": book_id, "author_id": author_id}


@pytest.fixture
def create_sample_genre(client):
    genre_data = {
        "name": "Fiction",
    }
    response = client.post("/api/v1/genres/", json=genre_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def associate_book_and_genre(client, create_sample_book, create_sample_genre):
    book_id = create_sample_book["id"]
    genre_id = create_sample_genre["id"]
    response = client.post(f"/api/v1/books/{book_id}/genres/{genre_id}")
    assert response.status_code == status.HTTP_201_CREATED
    return {"book_id": book_id, "genre_id": genre_id}


# Test for fetching all books
def test_get_books(client):
    response = client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# Test for fetching a book by ID
def test_get_book_by_id(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.get(f"/api/v1/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == book_id


# Test for attempting to fetch a non-existent book
def test_get_nonexistent_book(client):
    response = client.get("/api/v1/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating a new book
def test_create_book(client):
    response = client.post("/api/v1/books/", json=valid_book_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["title"] == valid_book_data["title"]


# Test for creating a book with duplicate ISBN
def test_create_book_with_duplicate_isbn(client, create_sample_book):
    duplicate_isbn_data = valid_book_data.copy()
    duplicate_isbn_data["isbn"] = create_sample_book["isbn"]  # Use the same ISBN
    response = client.post("/api/v1/books/", json=duplicate_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# Test for updating a book
def test_update_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    updated_data = {"title": "Updated Title", "isbn": "1234567890123"}
    response = client.patch(f"/api/v1/books/{book_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == updated_data["title"]


# Test for updating a non-existent book
def test_update_nonexistent_book(client):
    updated_data = {"title": "Updated Title"}
    response = client.patch("/api/v1/books/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for updating a book with invalid ISBN
def test_update_book_with_invalid_isbn(client, create_sample_book):
    another_book = valid_book_data.copy()
    another_book["isbn"] = "1234567890124"
    client.post("/api/v1/books/", json=another_book)
    book_id = create_sample_book["id"]
    invalid_isbn_data = {"isbn": "1234567890124"}
    response = client.patch(f"/api/v1/books/{book_id}", json=invalid_isbn_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "ISBN must be unique"}


# Test for deleting a book
def test_delete_book(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/api/v1/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the book is really deleted
    response = client.get(f"/api/v1/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for attempting to delete a non-existent book
def test_delete_nonexistent_book(client):
    response = client.delete("/api/v1/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for getting authors of a book
def test_get_authors_of_book(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    response = client.get(f"/api/v1/books/{book_id}/authors")
    assert response.status_code == status.HTTP_200_OK
    authors = response.json()["items"]
    assert isinstance(authors, list)
    assert len(authors) > 0
    assert authors[0]["name"] == "Jane"


# Test for getting authors of a non-existent book
def test_get_authors_of_nonexistent_book(client):
    response = client.get("/api/v1/books/999999/authors")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating a book-author association
def test_create_book_author_association(
    client, create_sample_book, create_sample_author
):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.post(f"/api/v1/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the association exists
    response = client.get(f"/api/v1/books/{book_id}/authors")
    authors = response.json()["items"]
    assert any(author["id"] == author_id for author in authors)


# Test for creating a duplicate book-author association
def test_create_duplicate_book_author_association(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    author_id = associate_book_and_author["author_id"]
    response = client.post(f"/api/v1/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Association already exists"}


# Test for creating an association with a non-existent book
def test_create_book_author_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.post(f"/api/v1/books/999999/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating an association with a non-existent author
def test_create_book_author_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.post(f"/api/v1/books/{book_id}/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for deleting a book-author association
def test_delete_book_author_association(client, associate_book_and_author):
    book_id = associate_book_and_author["book_id"]
    author_id = associate_book_and_author["author_id"]
    response = client.delete(f"/api/v1/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the association is removed
    response = client.get(f"/api/v1/books/{book_id}/authors")
    authors = response.json()["items"]
    assert not any(author["id"] == author_id for author in authors)


# Test for deleting a non-existent book-author association
def test_delete_nonexistent_book_author_association(
    client, create_sample_book, create_sample_author
):
    book_id = create_sample_book["id"]
    author_id = create_sample_author["id"]
    response = client.delete(f"/api/v1/books/{book_id}/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Association not found"}


# Test for deleting an association with a non-existent book
def test_delete_book_author_association_nonexistent_book(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.delete(f"/api/v1/books/999999/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for deleting an association with a non-existent author
def test_delete_book_author_association_nonexistent_author(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/api/v1/books/{book_id}/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# Test for getting genres of a book
def test_get_genres_of_book(client, associate_book_and_genre):
    book_id = associate_book_and_genre["book_id"]
    response = client.get(f"/api/v1/books/{book_id}/genres")
    assert response.status_code == status.HTTP_200_OK
    genres = response.json()["items"]
    assert isinstance(genres, list)
    assert len(genres) > 0
    assert genres[0]["name"] == "Fiction"


# Test for getting genres of a non-existent book
def test_get_genres_of_nonexistent_book(client):
    response = client.get("/api/v1/books/999999/genres")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating a book-genre association
def test_create_book_genre_association(client, create_sample_book, create_sample_genre):
    book_id = create_sample_book["id"]
    genre_id = create_sample_genre["id"]
    response = client.post(f"/api/v1/books/{book_id}/genres/{genre_id}")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the association exists
    response = client.get(f"/api/v1/books/{book_id}/genres")
    genres = response.json()["items"]
    assert any(genre["id"] == genre_id for genre in genres)


# Test for creating a duplicate book-genre association
def test_create_duplicate_book_genre_association(client, associate_book_and_genre):
    book_id = associate_book_and_genre["book_id"]
    genre_id = associate_book_and_genre["genre_id"]
    response = client.post(f"/api/v1/books/{book_id}/genres/{genre_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Association already exists"}


# Test for creating an association with a non-existent book
def test_create_book_genre_association_nonexistent_book(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.post(f"/api/v1/books/999999/genres/{genre_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for creating an association with a non-existent genre
def test_create_book_genre_association_nonexistent_genre(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.post(f"/api/v1/books/{book_id}/genres/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for deleting a book-genre association
def test_delete_book_genre_association(client, associate_book_and_genre):
    book_id = associate_book_and_genre["book_id"]
    genre_id = associate_book_and_genre["genre_id"]
    response = client.delete(f"/api/v1/books/{book_id}/genres/{genre_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the association is removed
    response = client.get(f"/api/v1/books/{book_id}/genres")
    genres = response.json()["items"]
    assert not any(genre["id"] == genre_id for genre in genres)


# Test for deleting a non-existent book-genre association
def test_delete_nonexistent_book_genre_association(
    client, create_sample_book, create_sample_genre
):
    book_id = create_sample_book["id"]
    genre_id = create_sample_genre["id"]
    response = client.delete(f"/api/v1/books/{book_id}/genres/{genre_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Association not found"}


# Test for deleting an association with a non-existent book
def test_delete_book_genre_association_nonexistent_book(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.delete(f"/api/v1/books/999999/genres/{genre_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for deleting an association with a non-existent genre
def test_delete_book_genre_association_nonexistent_genre(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/api/v1/books/{book_id}/genres/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


def test_sort_books_by_title_ascending(client):
    titles = ["TestTitle C", "TestTitle A", "TestTitle B"]
    created_ids = []
    for idx, title in enumerate(titles):
        book_data = valid_book_data.copy()
        book_data["title"] = title
        book_data["isbn"] = str(int(valid_book_data["isbn"]) + idx + 1)
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_ids.append(response.json()["id"])

    response = client.get("/api/v1/books/?sort_by=title&sort_order=asc")
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]

    sorted_books = [book for book in books if book["id"] in created_ids]
    sorted_titles = [book["title"] for book in sorted_books]
    expected_order = sorted(sorted_titles)
    assert (
        sorted_titles == expected_order
    ), f"Expected order: {expected_order}, got: {sorted_titles}"


def test_sort_books_by_year_descending(client):
    years = [1990, 2000, 1980]
    created_ids = []
    for idx, year in enumerate(years):
        book_data = valid_book_data.copy()
        book_data["title"] = f"TestYearBook {year}"
        book_data["year_of_publication"] = year

        book_data["isbn"] = str(int(valid_book_data["isbn"]) + (idx + 10))
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_ids.append(response.json()["id"])

    response = client.get("/api/v1/books/?sort_by=year_of_publication&sort_order=desc")
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]

    sorted_books = [book for book in books if book["id"] in created_ids]
    sorted_years = [book["year_of_publication"] for book in sorted_books]
    expected_order = sorted(sorted_years, reverse=True)
    assert (
        sorted_years == expected_order
    ), f"Expected order: {expected_order}, got: {sorted_years}"


# Test for sorting authors by name in ascending order for a given book
def test_sort_authors_by_name_ascending(client, create_sample_book):
    book_id = create_sample_book["id"]
    authors = [
        {"name": "Charlie", "surname": "Smith", "year_of_birth": 1970},
        {"name": "Alice", "surname": "Johnson", "year_of_birth": 1985},
        {"name": "Bob", "surname": "Williams", "year_of_birth": 1990},
    ]
    created_author_ids = []
    for author in authors:
        response = client.post("/api/v1/authors/", json=author)
        assert response.status_code == status.HTTP_201_CREATED
        author_obj = response.json()
        created_author_ids.append(author_obj["id"])
        resp_assoc = client.post(f"/api/v1/books/{book_id}/authors/{author_obj['id']}")
        assert resp_assoc.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/api/v1/books/{book_id}/authors?sort_by=name&sort_order=asc"
    )
    assert response.status_code == status.HTTP_200_OK
    result_authors = response.json()["items"]
    filtered_authors = [a for a in result_authors if a["id"] in created_author_ids]
    sorted_names = [author["name"] for author in filtered_authors]
    expected_sorted_names = sorted(sorted_names)
    assert (
        sorted_names == expected_sorted_names
    ), f"Expected order: {expected_sorted_names}, got: {sorted_names}"


# Test for sorting authors by year_of_birth in descending order for a given book
def test_sort_authors_by_year_of_birth_descending(client, create_sample_book):
    book_id = create_sample_book["id"]
    authors = [
        {"name": "Author A", "surname": "X", "year_of_birth": 1960},
        {"name": "Author B", "surname": "Y", "year_of_birth": 1980},
        {"name": "Author C", "surname": "Z", "year_of_birth": 1970},
    ]
    created_author_ids = []
    for author in authors:
        response = client.post("/api/v1/authors/", json=author)
        assert response.status_code == status.HTTP_201_CREATED
        author_obj = response.json()
        created_author_ids.append(author_obj["id"])
        resp_assoc = client.post(f"/api/v1/books/{book_id}/authors/{author_obj['id']}")
        assert resp_assoc.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/api/v1/books/{book_id}/authors?sort_by=year_of_birth&sort_order=desc"
    )
    assert response.status_code == status.HTTP_200_OK
    result_authors = response.json()["items"]

    filtered_authors = [a for a in result_authors if a["id"] in created_author_ids]
    sorted_years = [author["year_of_birth"] for author in filtered_authors]
    expected_sorted_years = sorted(sorted_years, reverse=True)
    assert (
        sorted_years == expected_sorted_years
    ), f"Expected order: {expected_sorted_years}, got: {sorted_years}"


# Test for sorting genres by name in ascending order for a given book
def test_sort_genres_by_name_ascending(client, create_sample_book):
    book_id = create_sample_book["id"]
    genres = [
        {"name": "Mystery"},
        {"name": "Adventure"},
        {"name": "Biography"},
    ]
    created_genre_ids = []
    for genre in genres:
        response = client.post("/api/v1/genres/", json=genre)
        assert response.status_code == status.HTTP_201_CREATED
        genre_obj = response.json()
        created_genre_ids.append(genre_obj["id"])
        resp_assoc = client.post(f"/api/v1/books/{book_id}/genres/{genre_obj['id']}")
        assert resp_assoc.status_code == status.HTTP_201_CREATED

    response = client.get(f"/api/v1/books/{book_id}/genres?sort_by=name&sort_order=asc")
    assert response.status_code == status.HTTP_200_OK
    result_genres = response.json()["items"]

    filtered_genres = [g for g in result_genres if g["id"] in created_genre_ids]
    sorted_names = [genre["name"] for genre in filtered_genres]
    expected_sorted_names = sorted(sorted_names)
    assert (
        sorted_names == expected_sorted_names
    ), f"Expected order: {expected_sorted_names}, got: {sorted_names}"


# Test for sorting genres by name in descending order for a given book
def test_sort_genres_by_name_descending(client, create_sample_book):
    book_id = create_sample_book["id"]
    genres = [
        {"name": "Romance"},
        {"name": "Horror"},
        {"name": "Sci-Fi"},
    ]
    created_genre_ids = []
    for genre in genres:
        response = client.post("/api/v1/genres/", json=genre)
        assert response.status_code == status.HTTP_201_CREATED
        genre_obj = response.json()
        created_genre_ids.append(genre_obj["id"])
        resp_assoc = client.post(f"/api/v1/books/{book_id}/genres/{genre_obj['id']}")
        assert resp_assoc.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/api/v1/books/{book_id}/genres?sort_by=name&sort_order=desc"
    )
    assert response.status_code == status.HTTP_200_OK
    result_genres = response.json()["items"]

    filtered_genres = [g for g in result_genres if g["id"] in created_genre_ids]
    sorted_names = [genre["name"] for genre in filtered_genres]
    expected_sorted_names = sorted(sorted_names, reverse=True)
    assert (
        sorted_names == expected_sorted_names
    ), f"Expected order: {expected_sorted_names}, got: {sorted_names}"
