from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict
from fastapi import Query

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
