from sqlalchemy.orm import Session
from sqlalchemy import select
from app.services.pagination import paginate
from app.models.book import Book
from app.models.author import Author
from app.models.book_author import BookAuthor
from app.models.genre import Genre
from app.models.book_genre import BookGenre
from app.schemas.api.v1.book import (
    CreateBookSchema,
    UpdateBookSchema,
    BookSortingSchema,
)
from app.schemas.pagination import PaginationParams
from app.services.sorting import apply_sorting
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_unique,
    ensure_association_does_not_exist,
    fetch_association,
)


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(
        self, pagination: PaginationParams, sorting_params: BookSortingSchema
    ):
        stmt = select(Book)
        if sorting_params.sort_by:
            sort_fields = {
                "title": Book.title,
                "description": Book.description,
                "year_of_publication": Book.year_of_publication,
                "isbn": Book.isbn,
                "series": Book.series,
                "file_link": Book.file_link,
                "edition": Book.edition,
                "created_at": Book.created_at,
                "updated_at": Book.updated_at,
            }
            stmt = apply_sorting(stmt, sorting_params, sort_fields)
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_book_by_id(self, book_id: int):
        return fetch_by_id(self.db, Book, book_id, "Book not found")

    def create_book(self, book_data: CreateBookSchema):
        ensure_unique(self.db, Book, "isbn", book_data.isbn, "ISBN must be unique")
        book = Book(**book_data.model_dump())
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def update_book(self, book_id: int, book_data: UpdateBookSchema):
        book = self.get_book_by_id(book_id)
        updated_data = book_data.model_dump(exclude_unset=True)

        if "isbn" in updated_data and updated_data["isbn"] != book.isbn:
            ensure_unique(
                self.db, Book, "isbn", updated_data["isbn"], "ISBN must be unique"
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
        fetch_by_id(self.db, Author, author_id, "Author not found")
        ensure_association_does_not_exist(
            self.db, BookAuthor, book_id=book_id, author_id=author_id
        )
        self.db.add(BookAuthor(book_id=book_id, author_id=author_id))
        self.db.commit()

    def remove_book_author_association(self, book_id: int, author_id: int):
        self.get_book_by_id(book_id)
        fetch_by_id(self.db, Author, author_id, "Author not found")
        association = fetch_association(
            self.db,
            BookAuthor,
            "Association not found",
            book_id=book_id,
            author_id=author_id,
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
        fetch_by_id(self.db, Genre, genre_id, "Genre not found")
        ensure_association_does_not_exist(
            self.db, BookGenre, book_id=book_id, genre_id=genre_id
        )
        self.db.add(BookGenre(book_id=book_id, genre_id=genre_id))
        self.db.commit()

    def remove_book_genre_association(self, book_id: int, genre_id: int):
        self.get_book_by_id(book_id)
        fetch_by_id(self.db, Genre, genre_id, "Genre not found")
        association = fetch_association(
            self.db,
            BookGenre,
            "Association not found",
            book_id=book_id,
            genre_id=genre_id,
        )
        self.db.delete(association)
        self.db.commit()
