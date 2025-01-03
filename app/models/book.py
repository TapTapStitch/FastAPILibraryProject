from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
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
