from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List


YearField = Field(..., ge=1000, le=9999)
ISBNField = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")


class AuthorInBookSchema(BaseModel):
    id: int
    name: str
    surname: str
    year_of_birth: int = YearField
    biography: str
    created_at: datetime
    updated_at: datetime


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = YearField
    isbn: str = ISBNField
    created_at: datetime
    updated_at: datetime
    authors: List[AuthorInBookSchema]


class CreateBookSchema(BaseModel):
    title: str
    description: str | None = ""
    year_of_publication: int = YearField
    isbn: str = ISBNField
    authors: List[int] | None = []

    model_config = ConfigDict(extra="forbid")


class UpdateBookSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    year_of_publication: int | None = Field(None, ge=1000, le=9999)
    isbn: str | None = Field(None, min_length=13, max_length=13, pattern=r"^\d{13}$")
    authors: List[int] | None = None

    model_config = ConfigDict(extra="forbid")
