from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class AuthorInBookSchema(BaseModel):
    id: int
    name: str
    surname: str
    year_of_birth: int = Field(..., ge=1000, le=9999)
    biography: str
    created_at: datetime
    updated_at: datetime


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = Field(..., ge=1000, le=9999)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")
    created_at: datetime
    updated_at: datetime
    authors: List[AuthorInBookSchema]


class ChangeBookSchema(BaseModel):
    title: str
    description: str | None = ""
    year_of_publication: int = Field(..., ge=1000, le=9999)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")
    authors: List[int] | None = []

    class Config:
        extra = "forbid"
