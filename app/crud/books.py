from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.book import Book
from ..models.author import Author
from ..models.book_author import BookAuthor
from ..schemas.book import CreateBookSchema, UpdateBookSchema
from ..schemas.pagination import PaginationParams


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, pagination: PaginationParams):
        stmt = select(Book).order_by(desc(Book.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_book_by_id(self, book_id: int):
        return self._fetch_book_by_id(book_id)

    def create_book(self, book_data: CreateBookSchema):
        self._ensure_isbn_unique(book_data.isbn)
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
        book = self._fetch_book_by_id(book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if "isbn" in updated_data and updated_data["isbn"] != book.isbn:
            self._ensure_isbn_unique(updated_data["isbn"])

        for field, value in updated_data.items():
            setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def remove_book(self, book_id: int):
        book = self._fetch_book_by_id(book_id)
        self.db.delete(book)
        self.db.commit()

    def get_authors_of_book(self, book_id: int, pagination: PaginationParams):
        self._fetch_book_by_id(book_id)
        stmt = (
            select(Author)
            .join(BookAuthor, Author.id == BookAuthor.author_id)
            .where(BookAuthor.book_id == book_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_book_author_association(self, book_id: int, author_id: int):
        self._fetch_book_by_id(book_id)
        self._ensure_author_exists(author_id)
        self._ensure_association_does_not_exist(book_id, author_id)
        book_author = BookAuthor(book_id=book_id, author_id=author_id)
        self.db.add(book_author)
        self.db.commit()

    def remove_book_author_association(self, book_id: int, author_id: int):
        self._fetch_book_by_id(book_id)
        self._ensure_author_exists(author_id)
        association = self._fetch_association(book_id, author_id)
        if not association:
            raise HTTPException(status_code=404, detail="Association not found")
        self.db.delete(association)
        self.db.commit()

    def _fetch_book_by_id(self, book_id: int):
        book = self.db.execute(
            select(Book).where(Book.id == book_id)
        ).scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def _ensure_isbn_unique(self, isbn: str):
        if self.db.execute(select(Book).where(Book.isbn == isbn)).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="ISBN must be unique")

    def _ensure_author_exists(self, author_id: int):
        if not self.db.execute(
            select(Author).where(Author.id == author_id)
        ).scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Author not found")

    def _ensure_association_does_not_exist(self, book_id: int, author_id: int):
        association_exists = self.db.execute(
            select(BookAuthor).filter_by(book_id=book_id, author_id=author_id)
        ).scalar_one_or_none()
        if association_exists:
            raise HTTPException(
                status_code=400,
                detail="Association already exists",
            )

    def _fetch_association(self, book_id: int, author_id: int):
        return self.db.execute(
            select(BookAuthor).filter_by(book_id=book_id, author_id=author_id)
        ).scalar_one_or_none()
