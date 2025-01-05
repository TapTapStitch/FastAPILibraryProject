from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from ..config import Base


class BookGenre(Base):
    __tablename__ = "book_genre"

    book_id = Column(
        Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True
    )
    genre_id = Column(
        Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(DateTime, default=func.now())
