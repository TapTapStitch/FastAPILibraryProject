from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..config import Base
from .book_author_association import book_author_association


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    year_of_birth = Column(Integer)
    biography = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    books = relationship(
        "Book",
        secondary=book_author_association,
        back_populates="authors",
        cascade="all, delete",
    )
