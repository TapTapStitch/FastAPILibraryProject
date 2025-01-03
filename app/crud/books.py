from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.book import Book
from ..schemas.book import CreateBookSchema, UpdateBookSchema


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, pagination):
        stmt = select(Book).order_by(desc(Book.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_book_by_id(self, book_id: int):
        book = self._get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def create_book(self, book_data: CreateBookSchema):
        self._check_isbn_unique(book_data.isbn)

        book = Book(
            title=book_data.title,
            description=book_data.description,
            year_of_publication=book_data.year_of_publication,
            isbn=book_data.isbn,
        )
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_data: UpdateBookSchema):
        book = self.get_book_by_id(book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if "isbn" in updated_data and updated_data["isbn"] != book.isbn:
            self._check_isbn_unique(updated_data["isbn"])

        for field, value in updated_data.items():
            setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def remove_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        self.db.delete(book)
        self.db.commit()

    def _get_book_by_id(self, book_id: int):
        return self.db.execute(
            select(Book).where(Book.id == book_id)
        ).scalar_one_or_none()

    def _check_isbn_unique(self, isbn: str):
        if self.db.execute(select(Book).where(Book.isbn == isbn)).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="ISBN must be unique")
