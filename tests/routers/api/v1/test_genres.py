import pytest
from fastapi import status

valid_genre_data = {"name": "Fiction"}


@pytest.fixture
def create_sample_genre(client):
    response = client.post("/api/v1/genres/", json=valid_genre_data)
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
    response = client.post("/api/v1/books/", json=book_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def associate_genre_and_book(client, create_sample_genre, create_sample_book):
    genre_id = create_sample_genre["id"]
    book_id = create_sample_book["id"]
    response = client.post(f"/api/v1/genres/{genre_id}/books/{book_id}")
    assert response.status_code == status.HTTP_201_CREATED
    return {"genre_id": genre_id, "book_id": book_id}


# Test for fetching all genres
def test_get_genres(client):
    response = client.get("/api/v1/genres/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# Test for fetching a genre by ID
def test_get_genre_by_id(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.get(f"/api/v1/genres/{genre_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == genre_id


# Test for attempting to fetch a non-existent genre
def test_get_nonexistent_genre(client):
    response = client.get("/api/v1/genres/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for creating a new genre
def test_create_genre(client):
    response = client.post("/api/v1/genres/", json=valid_genre_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["name"] == valid_genre_data["name"]


# Test for creating a genre with missing data
def test_create_genre_with_missing_data(client):
    invalid_genre_data = {}
    response = client.post("/api/v1/genres/", json=invalid_genre_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# Test for updating a genre
def test_update_genre(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    updated_data = {"name": "Updated Genre"}
    response = client.patch(f"/api/v1/genres/{genre_id}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == updated_data["name"]


# Test for updating a non-existent genre
def test_update_nonexistent_genre(client):
    updated_data = {"name": "Updated Genre"}
    response = client.patch("/api/v1/genres/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for deleting a genre
def test_delete_genre(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.delete(f"/api/v1/genres/{genre_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the genre is really deleted
    response = client.get(f"/api/v1/genres/{genre_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for attempting to delete a non-existent genre
def test_delete_nonexistent_genre(client):
    response = client.delete("/api/v1/genres/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for getting books of a genre
def test_get_books_of_genre(client, associate_genre_and_book):
    genre_id = associate_genre_and_book["genre_id"]
    response = client.get(f"/api/v1/genres/{genre_id}/books")
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]
    assert isinstance(books, list)
    assert len(books) > 0
    assert books[0]["title"] == "Sample Book"


# Test for getting books of a non-existent genre
def test_get_books_of_nonexistent_genre(client):
    response = client.get("/api/v1/genres/999999/books")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for creating a genre-book association
def test_create_genre_book_association(client, create_sample_genre, create_sample_book):
    genre_id = create_sample_genre["id"]
    book_id = create_sample_book["id"]
    response = client.post(f"/api/v1/genres/{genre_id}/books/{book_id}")
    assert response.status_code == status.HTTP_201_CREATED

    # Verify the association exists
    response = client.get(f"/api/v1/genres/{genre_id}/books")
    books = response.json()["items"]
    assert any(book["id"] == book_id for book in books)


# Test for creating a duplicate genre-book association
def test_create_duplicate_genre_book_association(client, associate_genre_and_book):
    genre_id = associate_genre_and_book["genre_id"]
    book_id = associate_genre_and_book["book_id"]
    response = client.post(f"/api/v1/genres/{genre_id}/books/{book_id}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"detail": "Association already exists"}


# Test for creating an association with a non-existent genre
def test_create_association_nonexistent_genre(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.post(f"/api/v1/genres/999999/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for creating an association with a non-existent book
def test_create_association_nonexistent_book(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.post(f"/api/v1/genres/{genre_id}/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


# Test for deleting a genre-book association
def test_delete_genre_book_association(client, associate_genre_and_book):
    genre_id = associate_genre_and_book["genre_id"]
    book_id = associate_genre_and_book["book_id"]
    response = client.delete(f"/api/v1/genres/{genre_id}/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify the association is removed
    response = client.get(f"/api/v1/genres/{genre_id}/books")
    books = response.json()["items"]
    assert not any(book["id"] == book_id for book in books)


# Test for deleting a non-existent genre-book association
def test_delete_nonexistent_genre_book_association(
    client, create_sample_genre, create_sample_book
):
    genre_id = create_sample_genre["id"]
    book_id = create_sample_book["id"]
    response = client.delete(f"/api/v1/genres/{genre_id}/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Association not found"}


# Test for deleting an association with a non-existent genre
def test_delete_association_nonexistent_genre(client, create_sample_book):
    book_id = create_sample_book["id"]
    response = client.delete(f"/api/v1/genres/999999/books/{book_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Genre not found"}


# Test for deleting an association with a non-existent book
def test_delete_association_nonexistent_book(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    response = client.delete(f"/api/v1/genres/{genre_id}/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Book not found"}


def test_sort_genres_by_name_ascending(client):
    names = ["Mystery", "Biography", "Fiction"]
    created_ids = []
    for idx, name in enumerate(names):
        genre_data = {
            "name": name,
            "description": f"{name} description",
        }
        response = client.post("/api/v1/genres/", json=genre_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_ids.append(response.json()["id"])

    response = client.get("/api/v1/genres/?sort_by=name&sort_order=asc")
    assert response.status_code == status.HTTP_200_OK
    genres = response.json()["items"]

    sorted_genres = [genre for genre in genres if genre["id"] in created_ids]
    sorted_names = [genre["name"] for genre in sorted_genres]
    expected_order = sorted(sorted_names)
    assert (
        sorted_names == expected_order
    ), f"Expected order: {expected_order}, got: {sorted_names}"


def test_sort_genres_by_name_descending(client):
    names = ["Mystery", "Biography", "Fiction"]
    created_ids = []
    for idx, name in enumerate(names):
        genre_data = {
            "name": name,
            "description": f"{name} description",
        }
        response = client.post("/api/v1/genres/", json=genre_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_ids.append(response.json()["id"])

    response = client.get("/api/v1/genres/?sort_by=name&sort_order=desc")
    assert response.status_code == status.HTTP_200_OK
    genres = response.json()["items"]

    sorted_genres = [genre for genre in genres if genre["id"] in created_ids]
    sorted_names = [genre["name"] for genre in sorted_genres]
    expected_order = sorted(sorted_names, reverse=True)
    assert (
        sorted_names == expected_order
    ), f"Expected order: {expected_order}, got: {sorted_names}"


# Test for sorting books of a genre by title in ascending order
def test_sort_books_of_genre_by_title_ascending(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    titles = ["Alpha", "Charlie", "Bravo"]
    created_ids = []
    for idx, title in enumerate(titles):
        book_data = {
            "title": title,
            "description": f"Description for {title}",
            "year_of_publication": 2023,
            "isbn": str(int("1234567890123") + idx + 1),
            "series": "Sample Series",
            "file_link": "https://example.com/sample.pdf",
            "edition": "First",
        }
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == status.HTTP_201_CREATED
        book_obj = response.json()
        created_ids.append(book_obj["id"])
        assoc_response = client.post(
            f"/api/v1/genres/{genre_id}/books/{book_obj['id']}"
        )
        assert assoc_response.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/api/v1/genres/{genre_id}/books?sort_by=title&sort_order=asc"
    )
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]
    sorted_books = [book for book in books if book["id"] in created_ids]
    sorted_titles = [book["title"] for book in sorted_books]
    expected_sorted_titles = sorted(sorted_titles)
    assert (
        sorted_titles == expected_sorted_titles
    ), f"Expected order: {expected_sorted_titles}, got: {sorted_titles}"


# Test for sorting books of a genre by year_of_publication in descending order
def test_sort_books_of_genre_by_year_descending(client, create_sample_genre):
    genre_id = create_sample_genre["id"]
    years = [1995, 2005, 1985]
    created_ids = []
    for idx, year in enumerate(years):
        book_data = {
            "title": f"Book {year}",
            "description": f"Description for book published in {year}",
            "year_of_publication": year,
            "isbn": str(int("1234567890123") + idx + 10),
            "series": "Sample Series",
            "file_link": "https://example.com/sample.pdf",
            "edition": "First",
        }
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == status.HTTP_201_CREATED
        book_obj = response.json()
        created_ids.append(book_obj["id"])
        assoc_response = client.post(
            f"/api/v1/genres/{genre_id}/books/{book_obj['id']}"
        )
        assert assoc_response.status_code == status.HTTP_201_CREATED

    response = client.get(
        f"/api/v1/genres/{genre_id}/books?sort_by=year_of_publication&sort_order=desc"
    )
    assert response.status_code == status.HTTP_200_OK
    books = response.json()["items"]

    sorted_books = [book for book in books if book["id"] in created_ids]
    sorted_years = [book["year_of_publication"] for book in sorted_books]
    expected_sorted_years = sorted(sorted_years, reverse=True)
    assert (
        sorted_years == expected_sorted_years
    ), f"Expected order: {expected_sorted_years}, got: {sorted_years}"
