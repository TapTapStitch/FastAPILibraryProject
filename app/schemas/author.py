from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class BookInAuthorSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = Field(..., ge=1000, le=9999)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")
    created_at: datetime
    updated_at: datetime


class AuthorSchema(BaseModel):
    id: int
    name: str
    surname: str
    year_of_birth: int = Field(..., ge=1000, le=9999)
    biography: str
    created_at: datetime
    updated_at: datetime
    books: List[BookInAuthorSchema]


class CreateAuthorSchema(BaseModel):
    name: str
    surname: str
    year_of_birth: int = Field(..., ge=1000, le=9999)
    biography: str | None = ""
    books: List[int] | None = []

    class Config:
        extra = "forbid"


class UpdateAuthorSchema(BaseModel):
    name: str | None = None
    surname: str | None = None
    year_of_birth: int | None = Field(None, ge=1000, le=9999)
    biography: str | None = None
    books: List[int] | None = None

    class Config:
        extra = "forbid"
