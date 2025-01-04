import pytest
from fastapi import status


valid_author_data = {"name": "John", "surname": "Doe", "year_of_birth": "1990"}


@pytest.fixture
def create_sample_author(client):
    response = client.post("/authors/", json=valid_author_data)
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


# 1. Test for fetching all authors
def test_get_authors(client):
    response = client.get("/authors/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()["items"], list)


# 2. Test for fetching an author by ID
def test_get_author_by_id(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == author_id


# 3. Test for attempting to fetch a non-existent author
def test_get_nonexistent_author(client):
    response = client.get("/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# 4. Test for creating a new author
def test_create_author(client):
    response = client.post("/authors/", json=valid_author_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()
    assert response.json()["name"] == valid_author_data["name"]


# 5. Test for creating an author with missing data
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


# 6. Test for updating an author
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


# 7. Test for updating a non-existent author
def test_update_nonexistent_author(client):
    updated_data = {"name": "Updated Name"}
    response = client.patch("/authors/999999", json=updated_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# 8. Test for deleting an author
def test_delete_author(client, create_sample_author):
    author_id = create_sample_author["id"]
    response = client.delete(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Check if the author is really deleted
    response = client.get(f"/authors/{author_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}


# 9. Test for attempting to delete a non-existent author
def test_delete_nonexistent_author(client):
    response = client.delete("/authors/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Author not found"}
