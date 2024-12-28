from pydantic import BaseModel
from datetime import datetime


class BookSchema(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime


class ChangeBookSchema(BaseModel):
    title: str
    description: str

    class Config:
        extra = "forbid"
