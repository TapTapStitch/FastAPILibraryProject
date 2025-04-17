from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query
from fastapi.openapi.models import Example

YearField = Field(..., ge=1000, le=9999)
ISBNField = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = YearField
    isbn: str = ISBNField
    series: str
    file_link: str
    edition: str
    created_at: datetime
    updated_at: datetime


class CreateBookSchema(BaseModel):
    title: str
    description: str | None = ""
    year_of_publication: int = YearField
    isbn: str = ISBNField
    series: str | None = ""
    file_link: str | None = ""
    edition: str | None = ""

    model_config = ConfigDict(extra="forbid")


class UpdateBookSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    year_of_publication: int | None = Field(None, ge=1000, le=9999)
    isbn: str | None = Field(None, min_length=13, max_length=13, pattern=r"^\d{13}$")
    series: str | None = None
    file_link: str | None = None
    edition: str | None = None

    model_config = ConfigDict(extra="forbid")


class BookSortingSchema(BaseModel):
    sort_by: (
        Literal[
            "title",
            "description",
            "year_of_publication",
            "isbn",
            "series",
            "file_link",
            "edition",
            "created_at",
            "updated_at",
        ]
        | None
    ) = Query(None)
    sort_order: Literal["asc", "desc"] | None = Query(None)


class BookSearchSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    year_of_publication: str | None = None
    isbn: str | None = None
    series: str | None = None
    file_link: str | None = None
    edition: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


def book_search_dependency(
    title: str | None = Query(
        default=None,
        description="Book title; supports operators: eq (default), ne, lt, lte, gt, gte, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Case-insensitive match",
                value="ilike:%python%",
            ),
            "example2": Example(
                summary="Exact title match",
                value="eq:Python 101",
            ),
            "example3": Example(
                summary="Title list",
                value="in:Python 101,Python Tricks",
            ),
        },
    ),
    description: str | None = Query(
        default=None,
        description="Book description; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Partial match on description",
                value="like:%advanced%",
            ),
            "example2": Example(
                summary="Case-insensitive search",
                value="ilike:%beginner%",
            ),
        },
    ),
    year_of_publication: str | None = Query(
        default=None,
        description="Year of publication; supports operators: eq (default), ne, lt, lte, gt, gte, in",
        openapi_examples={
            "example1": Example(
                summary="Published after 2010",
                value="gte:2010",
            ),
            "example2": Example(
                summary="Exact year match",
                value="eq:2015",
            ),
            "example3": Example(
                summary="Year range",
                value="in:2010,2015,2020",
            ),
        },
    ),
    isbn: str | None = Query(
        default=None,
        description="ISBN number; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Exact ISBN",
                value="eq:9783161484100",
            ),
            "example2": Example(
                summary="Partial ISBN match",
                value="like:%1484100",
            ),
        },
    ),
    series: str | None = Query(
        default=None,
        description="Book series; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Exact series match",
                value="eq:Harry Potter",
            ),
            "example2": Example(
                summary="Case-insensitive search",
                value="ilike:%rings%",
            ),
        },
    ),
    file_link: str | None = Query(
        default=None,
        description="File link; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Partial URL match",
                value="like:%google.com%",
            ),
            "example2": Example(
                summary="Case-insensitive match",
                value="ilike:%dropbox%",
            ),
        },
    ),
    edition: str | None = Query(
        default=None,
        description="Edition; supports operators: eq (default), ne, like, ilike, in",
        openapi_examples={
            "example1": Example(
                summary="Exact edition match",
                value="eq:2nd",
            ),
            "example2": Example(
                summary="Edition search",
                value="ilike:%revised%",
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
                summary="Exact creation date",
                value="eq:2022-06-15T00:00:00",
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
                summary="Not equal to update date",
                value="ne:2023-06-15T00:00:00",
            ),
        },
    ),
) -> BookSearchSchema:
    return BookSearchSchema(
        title=title,
        description=description,
        year_of_publication=year_of_publication,
        isbn=isbn,
        series=series,
        file_link=file_link,
        edition=edition,
        created_at=created_at,
        updated_at=updated_at,
    ).model_dump(exclude_none=True)
