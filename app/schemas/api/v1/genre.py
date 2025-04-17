from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict
from fastapi import Query
from fastapi.openapi.models import Example


class GenreSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class CreateGenreSchema(BaseModel):
    name: str
    description: str | None = ""

    model_config = ConfigDict(extra="forbid")


class UpdateGenreSchema(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(extra="forbid")


class GenreSortingSchema(BaseModel):
    sort_by: (
        Literal[
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        | None
    ) = Query(None)
    sort_order: Literal["asc", "desc"] | None = Query(None)


class GenreSearchSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


def genre_search_dependency(
    name: str | None = Query(
        default=None,
        description="Genre name; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Case-insensitive match",
                value="ilike:%fantasy%",
            ),
            "example2": Example(
                summary="Exact match",
                value="eq:fantasy",
            ),
            "example3": Example(
                summary="Multiple values",
                value="in:fantasy,drama,romance",
            ),
        },
    ),
    description: str | None = Query(
        default=None,
        description="Genre description; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Partial match",
                value="like:%myth%",
            ),
            "example2": Example(
                summary="Case-insensitive description",
                value="ilike:%legend%",
            ),
        },
    ),
    created_at: str | None = Query(
        default=None,
        description="Creation timestamp; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="Before a specific date",
                value="lt:2023-01-01T00:00:00",
            ),
            "example2": Example(
                summary="Exact timestamp match",
                value="eq:2022-12-25T00:00:00",
            ),
            "example3": Example(
                summary="Between a range of dates",
                value="in:2022-01-01T00:00:00,2022-12-31T23:59:59",
            ),
        },
    ),
    updated_at: str | None = Query(
        default=None,
        description="Update timestamp; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="After a specific date",
                value="gte:2022-01-01T00:00:00",
            ),
            "example2": Example(
                summary="Not equal to a specific update date",
                value="ne:2023-06-15T00:00:00",
            ),
        },
    ),
) -> GenreSearchSchema:
    return GenreSearchSchema(
        name=name,
        description=description,
        created_at=created_at,
        updated_at=updated_at,
    ).model_dump(exclude_none=True)
