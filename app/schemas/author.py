from pydantic import BaseModel, Field
from datetime import datetime


class AuthorSchema(BaseModel):
    id: int
    name: str
    surname: str
    year_of_birth: int = Field(..., ge=1000, le=9999)
    biography: str
    created_at: datetime
    updated_at: datetime


class ChangeAuthorSchema(BaseModel):
    name: str
    surname: str
    year_of_birth: int = Field(..., ge=1000, le=9999)
    biography: str | None = ""

    class Config:
        extra = "forbid"
