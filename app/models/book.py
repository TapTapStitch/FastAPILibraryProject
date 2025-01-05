from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.book_author import BookAuthor
from app.models.book_genre import BookGenre
from ..config import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    year_of_publication = Column(Integer)
    isbn = Column(String, unique=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    authors = relationship("Author", secondary="book_author", back_populates="books")
    genres = relationship("Genre", secondary="book_genre", back_populates="books")
