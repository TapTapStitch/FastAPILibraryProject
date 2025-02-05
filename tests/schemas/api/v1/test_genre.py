from datetime import datetime
import pytest
from pydantic import ValidationError
from app.schemas.api.v1.genre import (
    GenreSchema,
    CreateGenreSchema,
    UpdateGenreSchema,
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
