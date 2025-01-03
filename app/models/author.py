from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..config import Base


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    year_of_birth = Column(Integer)
    biography = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
