from pydantic import BaseModel, ConfigDict
from datetime import datetime


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
