from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query

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
