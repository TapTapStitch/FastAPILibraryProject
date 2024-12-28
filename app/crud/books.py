from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.book import Book


class BooksCrud:
    def get_books(self, db: Session):
        return db.query(Book).all()

    def get_book_by_id(self, db: Session, book_id: int):
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def create_book(self, db: Session, title: str, description: str):
        book = Book(title=title, description=description)
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def remove_book(self, db: Session, book_id: int):
        book = self.get_book_by_id(db=db, book_id=book_id)
        db.delete(book)
        db.commit()

    def update_book(self, db: Session, book_id: int, title: str, description: str):
        book = self.get_book_by_id(db=db, book_id=book_id)
        book.title = title
        book.description = description
        db.commit()
        db.refresh(book)
        return book
