from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.book import Book
from ..models.author import Author
from ..models.book_author import BookAuthor
from ..models.genre import Genre
from ..models.book_genre import BookGenre
from ..schemas.book import CreateBookSchema, UpdateBookSchema
from ..schemas.pagination import PaginationParams


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(self, pagination: PaginationParams):
        stmt = select(Book).order_by(desc(Book.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_book_by_id(self, book_id: int):
        return self._fetch_by_id(Book, book_id, "Book not found")

    def create_book(self, book_data: CreateBookSchema):
        self._ensure_unique(Book, "isbn", book_data.isbn, "ISBN must be unique")
        book = Book(**book_data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_data: UpdateBookSchema):
        book = self.get_book_by_id(book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if "isbn" in updated_data and updated_data["isbn"] != book.isbn:
            self._ensure_unique(
                Book, "isbn", updated_data["isbn"], "ISBN must be unique"
            )

        for field, value in updated_data.items():
            setattr(book, field, value)

        self.db.commit()
        self.db.refresh(book)
        return book

    def remove_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        self.db.delete(book)
        self.db.commit()

    def get_authors_of_book(self, book_id: int, pagination: PaginationParams):
        self.get_book_by_id(book_id)
        stmt = (
            select(Author)
            .join(BookAuthor, Author.id == BookAuthor.author_id)
            .where(BookAuthor.book_id == book_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_book_author_association(self, book_id: int, author_id: int):
        self.get_book_by_id(book_id)
        self._fetch_by_id(Author, author_id, "Author not found")
        self._ensure_association_does_not_exist(
            BookAuthor, book_id=book_id, author_id=author_id
        )
        self.db.add(BookAuthor(book_id=book_id, author_id=author_id))
        self.db.commit()

    def remove_book_author_association(self, book_id: int, author_id: int):
        self.get_book_by_id(book_id)
        self._fetch_by_id(Author, author_id, "Author not found")
        association = self._fetch_association(
            BookAuthor, "Association not found", book_id=book_id, author_id=author_id
        )
        self.db.delete(association)
        self.db.commit()

    def get_genres_of_book(self, book_id: int, pagination: PaginationParams):
        self.get_book_by_id(book_id)
        stmt = (
            select(Genre)
            .join(BookGenre, Genre.id == BookGenre.genre_id)
            .where(BookGenre.book_id == book_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_book_genre_association(self, book_id: int, genre_id: int):
        self.get_book_by_id(book_id)
        self._fetch_by_id(Genre, genre_id, "Genre not found")
        self._ensure_association_does_not_exist(
            BookGenre, book_id=book_id, genre_id=genre_id
        )
        self.db.add(BookGenre(book_id=book_id, genre_id=genre_id))
        self.db.commit()

    def remove_book_genre_association(self, book_id: int, genre_id: int):
        self.get_book_by_id(book_id)
        self._fetch_by_id(Genre, genre_id, "Genre not found")
        association = self._fetch_association(
            BookGenre, "Association not found", book_id=book_id, genre_id=genre_id
        )
        self.db.delete(association)
        self.db.commit()

    def _fetch_by_id(self, model, item_id, not_found_message):
        item = self.db.execute(
            select(model).where(model.id == item_id)
        ).scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=404, detail=not_found_message)
        return item

    def _ensure_unique(self, model, field, value, error_message):
        if self.db.execute(
            select(model).where(getattr(model, field) == value)
        ).scalar_one_or_none():
            raise HTTPException(status_code=400, detail=error_message)

    def _ensure_association_does_not_exist(self, model, **kwargs):
        if self.db.execute(select(model).filter_by(**kwargs)).scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Association already exists")

    def _fetch_association(self, model, not_found_message, **kwargs):
        association = self.db.execute(
            select(model).filter_by(**kwargs)
        ).scalar_one_or_none()
        if not association:
            raise HTTPException(status_code=404, detail=not_found_message)
        return association
