from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query
from fastapi.openapi.models import Example

YearField = Field(..., ge=1000, le=9999)


class AuthorSchema(BaseModel):
    id: int
    name: str
    surname: str
    year_of_birth: int = YearField
    biography: str
    created_at: datetime
    updated_at: datetime


class CreateAuthorSchema(BaseModel):
    name: str
    surname: str
    year_of_birth: int = YearField
    biography: str | None = ""

    model_config = ConfigDict(extra="forbid")


class UpdateAuthorSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    year_of_birth: int | None = Field(None, ge=1000, le=9999)
    biography: str | None = None

    model_config = ConfigDict(extra="forbid")


class AuthorSortingSchema(BaseModel):
    sort_by: (
        Literal[
            "name",
            "surname",
            "year_of_birth",
            "biography",
            "created_at",
            "updated_at",
        ]
        | None
    ) = Query(None)
    sort_order: Literal["asc", "desc"] | None = Query(None)


class AuthorSearchSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    year_of_birth: str | None = None
    biography: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


def author_search_dependency(
    name: str | None = Query(
        default=None,
        description="Author's name; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Case-insensitive name search",
                value="ilike:%john%",
            ),
            "example2": Example(
                summary="Exact name match",
                value="eq:John",
            ),
            "example3": Example(
                summary="Multiple names",
                value="in:John,Jane,Mark",
            ),
        },
    ),
    surname: str | None = Query(
        default=None,
        description="Author's surname; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Partial surname match",
                value="like:%doe%",
            ),
            "example2": Example(
                summary="Case-insensitive surname search",
                value="ilike:%smith%",
            ),
        },
    ),
    year_of_birth: str | None = Query(
        default=None,
        description="Year of birth; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="Born after 1950",
                value="gte:1950",
            ),
            "example2": Example(
                summary="Exact birth year",
                value="eq:1975",
            ),
            "example3": Example(
                summary="Multiple birth years",
                value="in:1950,1960,1970",
            ),
        },
    ),
    biography: str | None = Query(
        default=None,
        description="Biography; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Mention of 'Nobel'",
                value="ilike:%Nobel%",
            ),
            "example2": Example(
                summary="Partial biography content",
                value="like:%poet%",
            ),
        },
    ),
    created_at: str | None = Query(
        default=None,
        description="Creation timestamp; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="Created before 2023",
                value="lt:2023-01-01T00:00:00",
            ),
            "example2": Example(
                summary="Exact creation timestamp",
                value="eq:2022-06-01T12:00:00",
            ),
        },
    ),
    updated_at: str | None = Query(
        default=None,
        description="Update timestamp; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="Updated after 2022",
                value="gte:2022-01-01T00:00:00",
            ),
            "example2": Example(
                summary="Exclude specific update timestamp",
                value="ne:2023-07-01T00:00:00",
            ),
        },
    ),
) -> AuthorSearchSchema:
    return AuthorSearchSchema(
        name=name,
        surname=surname,
        year_of_birth=year_of_birth,
        biography=biography,
        created_at=created_at,
        updated_at=updated_at,
    ).model_dump(exclude_none=True)
