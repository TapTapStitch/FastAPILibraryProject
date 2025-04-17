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
from app.schemas.api.v1.author import AuthorSortingSchema
from app.schemas.api.v1.genre import GenreSortingSchema
from app.schemas.pagination import PaginationParams
from app.services.sorting import apply_sorting
from app.services.search import apply_filters
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_unique,
    ensure_association_does_not_exist,
    fetch_association,
)
from app.crud.api.v1.shared.sort_fields import (
    book_sort_fields,
    author_sort_fields,
    genre_sort_fields,
)
from app.crud.api.v1.shared.search_filelds import (
    book_search_fields,
    author_search_fields,
    genre_search_fields,
)


class BooksCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_books(
        self,
        filters: dict,
        sorting_params: BookSortingSchema,
        pagination: PaginationParams,
    ):
        stmt = select(Book)
        if any(filters):
            stmt = apply_filters(stmt, filters, book_search_fields)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, book_sort_fields)
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

    def get_authors_of_book(
        self,
        book_id: int,
        filters: dict,
        sorting_params: AuthorSortingSchema,
        pagination: PaginationParams,
    ):
        self.get_book_by_id(book_id)
        stmt = (
            select(Author)
            .join(BookAuthor, Author.id == BookAuthor.author_id)
            .where(BookAuthor.book_id == book_id)
        )
        if any(filters):
            stmt = apply_filters(stmt, filters, author_search_fields)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, author_sort_fields)
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

    def get_genres_of_book(
        self,
        book_id: int,
        filters: dict,
        sorting_params: GenreSortingSchema,
        pagination: PaginationParams,
    ):
        self.get_book_by_id(book_id)
        stmt = (
            select(Genre)
            .join(BookGenre, Genre.id == BookGenre.genre_id)
            .where(BookGenre.book_id == book_id)
        )
        if any(filters):
            stmt = apply_filters(stmt, filters, genre_search_fields)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, genre_sort_fields)
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
