from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.api.v1.genre import (
    GenreSchema,
    CreateGenreSchema,
    UpdateGenreSchema,
    GenreSortingSchema,
)


def test_genre_schema():
    # Valid data
    genre = GenreSchema(
        id=1,
        name="Science Fiction",
        description="A genre of speculative fiction.",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    assert genre.name == "Science Fiction"

    # Invalid data type for id
    with pytest.raises(ValidationError):
        GenreSchema(
            id="one",  # Invalid id type
            name="Science Fiction",
            description="A genre of speculative fiction.",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )


def test_create_genre_schema():
    # Valid data
    genre_data = CreateGenreSchema(
        name="Fantasy", description="A genre of magical realism."
    )
    assert genre_data.name == "Fantasy"

    # Missing required field 'name'
    with pytest.raises(ValidationError):
        CreateGenreSchema(description="A genre of magical realism.")


def test_update_genre_schema():
    # Valid data
    genre_data = UpdateGenreSchema(
        name="Horror",
    )
    assert genre_data.name == "Horror"

    # Extra fields should raise an error due to `extra="forbid"`
    with pytest.raises(ValidationError):
        UpdateGenreSchema(name="Horror", extra_field="Not allowed")


@pytest.mark.parametrize(
    "params, is_valid",
    [
        ({"sort_by": "name", "sort_order": "asc"}, True),
        ({"sort_by": "description", "sort_order": "desc"}, True),
        ({"sort_by": None, "sort_order": None}, True),
        ({"sort_by": "invalid_field", "sort_order": "asc"}, False),
        ({"sort_by": "name", "sort_order": "invalid_order"}, False),
    ],
)
def test_genre_sorting_schema(params, is_valid):
    if is_valid:
        schema = GenreSortingSchema(**params)
        assert schema.sort_by == params["sort_by"]
        assert schema.sort_order == params["sort_order"]
    else:
        with pytest.raises(ValidationError):
            GenreSortingSchema(**params)
