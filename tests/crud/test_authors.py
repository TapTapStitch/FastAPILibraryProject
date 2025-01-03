import pytest
from fastapi import HTTPException
from app.crud.authors import AuthorsCrud
from app.schemas.author import CreateAuthorSchema, UpdateAuthorSchema
from app.models.author import Author


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
