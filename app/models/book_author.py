from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.config import Base


class BookAuthor(Base):
    __tablename__ = "book_author"

    book_id = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    author_id = Column(
        Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(DateTime, default=func.now())
