from sqlalchemy import Column, Integer, ForeignKey, Table
from ..config import Base

book_author_association = Table(
    "book_author_association",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)
