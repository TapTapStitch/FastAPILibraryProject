from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from ..models.book import Book
from ..schemas.book import ChangeBookSchema


class BooksCrud:
    def get_books(self, db: Session):
        return db.query(Book).order_by(desc(Book.created_at))

    def get_book_by_id(self, db: Session, book_id: int):
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def create_book(self, db: Session, book_data: ChangeBookSchema):
        if db.query(Book).filter(Book.isbn == book_data.isbn).first():
            raise HTTPException(status_code=400, detail="ISBN must be unique")

        book = Book(**book_data.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    def remove_book(self, db: Session, book_id: int):
        book = self.get_book_by_id(db=db, book_id=book_id)
        db.delete(book)
        db.commit()

    def update_book(self, db: Session, book_id: int, book_data: ChangeBookSchema):
        book = self.get_book_by_id(db=db, book_id=book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if updated_data["isbn"] != book.isbn:
            existing_book = (
                db.query(Book).filter(Book.isbn == updated_data["isbn"]).first()
            )
            if existing_book:
                raise HTTPException(status_code=400, detail="ISBN must be unique")

        for field, value in updated_data.items():
            setattr(book, field, value)
        db.commit()
        db.refresh(book)
        return book
