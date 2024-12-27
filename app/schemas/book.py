from pydantic import BaseModel


class BookSchema(BaseModel):
    id: int
    title: str
    description: str


class ChangeBookSchema(BaseModel):
    title: str
    description: str
