from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: str


class BookCreateSchema(BaseModel):
    title: str
    description: str | None = None


class BookUpdateSchema(BaseModel):
    title: str
    description: str | None = None
