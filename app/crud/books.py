from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc, select
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
        book = self._get_book_by_id(book_id)
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    def create_book(self, book_data: CreateBookSchema):
        self._check_isbn_unique(book_data.isbn)

        authors = self._get_authors_by_ids(book_data.authors)
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
            self._check_isbn_unique(updated_data["isbn"])

        if "authors" in updated_data:
            authors = self._get_authors_by_ids(book_data.authors)
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

    def _get_book_by_id(self, book_id: int):
        return self.db.execute(
            select(Book).options(selectinload(Book.authors)).where(Book.id == book_id)
        ).scalar_one_or_none()

    def _check_isbn_unique(self, isbn: str):
        if self.db.execute(select(Book).where(Book.isbn == isbn)).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="ISBN must be unique")

    def _get_authors_by_ids(self, author_ids: list):
        return (
            self.db.execute(select(Author).where(Author.id.in_(author_ids)))
            .scalars()
            .all()
        )
