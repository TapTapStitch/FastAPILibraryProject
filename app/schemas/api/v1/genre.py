from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict
from fastapi import Query


class GenreSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class CreateGenreSchema(BaseModel):
    name: str
    description: str | None = ""

    model_config = ConfigDict(extra="forbid")


class UpdateGenreSchema(BaseModel):
    name: str | None = None
    description: str | None = None

    model_config = ConfigDict(extra="forbid")


class GenreSortingSchema(BaseModel):
    sort_by: (
        Literal[
            "name",
            "description",
            "created_at",
            "updated_at",
        ]
        | None
    ) = Query(None)
    sort_order: Literal["asc", "desc"] | None = Query(None)
