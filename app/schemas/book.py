from typing import Optional
from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class BookCreateSchema(BaseModel):
    title: str
    description: Optional[str] = None


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
