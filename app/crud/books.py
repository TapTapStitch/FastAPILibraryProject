from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from ..models.book import Book
from ..models.author import Author
from ..schemas.book import CreateBookSchema, UpdateBookSchema


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self):
        books = (
            self.db.query(Book)
            .options(selectinload(Book.authors))
            .order_by(desc(Book.created_at))
        )
        return paginate(books)

    def get_book_by_id(self, book_id: int):
        book = self.db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def create_book(self, book_data: CreateBookSchema):
        if self.db.query(Book).filter(Book.isbn == book_data.isbn).first():
            raise HTTPException(status_code=400, detail="ISBN must be unique")

        authors = self.db.query(Author).filter(Author.id.in_(book_data.authors)).all()

        if len(authors) != len(book_data.authors):
            raise HTTPException(status_code=404, detail="One or more authors not found")

        book = Book(
            title=book_data.title,
            description=book_data.description,
            year_of_publication=book_data.year_of_publication,
            isbn=book_data.isbn,
            authors=authors,
        )
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_data: UpdateBookSchema):
        book = self.get_book_by_id(book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if "isbn" in updated_data and updated_data["isbn"] != book.isbn:
            existing_book = (
                self.db.query(Book).filter(Book.isbn == updated_data["isbn"]).first()
            )
            if existing_book:
                raise HTTPException(status_code=400, detail="ISBN must be unique")

        if "authors" in updated_data:
            authors = (
                self.db.query(Author).filter(Author.id.in_(book_data.authors)).all()
            )
            if len(authors) != len(book_data.authors):
                raise HTTPException(
                    status_code=404, detail="One or more authors not found"
                )
            updated_data["authors"] = authors

        for field, value in updated_data.items():
            setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def remove_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        self.db.delete(book)
        self.db.commit()
