from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.api.v1.author import (
    AuthorSchema,
    CreateAuthorSchema,
    UpdateAuthorSchema,
    AuthorSortingSchema,
)


def test_author_schema():
    # Valid data
    author = AuthorSchema(
        id=1,
        name="Jane",
        surname="Doe",
        year_of_birth=1985,
        biography="Biography of Jane Doe.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert author.name == "Jane"

    # Invalid year_of_birth
    with pytest.raises(ValidationError):
        AuthorSchema(
            id=1,
            name="Jane",
            surname="Doe",
            year_of_birth=999,  # Invalid year
            biography="Biography of Jane Doe.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


def test_create_author_schema():
    # Valid data
    author_data = CreateAuthorSchema(
        name="Jane", surname="Doe", year_of_birth=1985, biography=""
    )
    assert author_data.name == "Jane"

    # Missing required field
    with pytest.raises(ValidationError):
        CreateAuthorSchema(surname="Doe", year_of_birth=1985, biography="")


def test_update_author_schema():
    # Valid data
    author_data = UpdateAuthorSchema(
        name="John",
    )
    assert author_data.name == "John"

    # Invalid year of birth
    with pytest.raises(ValidationError):
        UpdateAuthorSchema(year_of_birth=999)  # Invalid year


@pytest.mark.parametrize(
    "params, is_valid",
    [
        ({"sort_by": "name", "sort_order": "asc"}, True),
        ({"sort_by": "year_of_birth", "sort_order": "desc"}, True),
        ({"sort_by": None, "sort_order": None}, True),
        ({"sort_by": "invalid_field", "sort_order": "asc"}, False),
        ({"sort_by": "name", "sort_order": "invalid_order"}, False),
    ],
)
def test_author_sorting_schema(params, is_valid):
    if is_valid:
        schema = AuthorSortingSchema(**params)
        assert schema.sort_by == params["sort_by"]
        assert schema.sort_order == params["sort_order"]
    else:
        with pytest.raises(ValidationError):
            AuthorSortingSchema(**params)
