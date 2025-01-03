from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


YearField = Field(..., ge=1000, le=9999)
ISBNField = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = YearField
    isbn: str = ISBNField
    created_at: datetime
    updated_at: datetime


class CreateBookSchema(BaseModel):
    title: str
    description: str | None = ""
    year_of_publication: int = YearField
    isbn: str = ISBNField

    model_config = ConfigDict(extra="forbid")


class UpdateBookSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    year_of_publication: int | None = Field(None, ge=1000, le=9999)
    isbn: str | None = Field(None, min_length=13, max_length=13, pattern=r"^\d{13}$")

    model_config = ConfigDict(extra="forbid")
