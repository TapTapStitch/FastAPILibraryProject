from sqlalchemy import Column, Integer, String, Text
from ..config import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
