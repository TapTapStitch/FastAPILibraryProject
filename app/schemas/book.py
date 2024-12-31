from pydantic import BaseModel, Field
from datetime import datetime


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    year_of_publication: int = Field(..., ge=1000, le=9999)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")
    created_at: datetime
    updated_at: datetime


class ChangeBookSchema(BaseModel):
    title: str
    description: str | None = ""
    year_of_publication: int = Field(..., ge=1000, le=9999)
    isbn: str = Field(..., min_length=13, max_length=13, pattern=r"^\d{13}$")

    class Config:
        extra = "forbid"
