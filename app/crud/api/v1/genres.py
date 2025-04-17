from sqlalchemy.orm import Session
from sqlalchemy import select
from app.services.pagination import paginate
from app.models.genre import Genre
from app.models.book import Book
from app.models.book_genre import BookGenre
from app.schemas.api.v1.genre import (
    CreateGenreSchema,
    UpdateGenreSchema,
    GenreSortingSchema,
)
from app.schemas.api.v1.book import BookSortingSchema
from app.schemas.pagination import PaginationParams
from app.services.sorting import apply_sorting
from app.services.search import apply_filters
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_association_does_not_exist,
    fetch_association,
)
from app.crud.api.v1.shared.sort_fields import book_sort_fields, genre_sort_fields
from app.crud.api.v1.shared.search_filelds import (
    book_search_fields,
    genre_search_fields,
)


class GenresCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_genres(
        self,
        filters: dict,
        sorting_params: GenreSortingSchema,
        pagination: PaginationParams,
    ):
        stmt = select(Genre)
        if any(filters):
            stmt = apply_filters(stmt, filters, genre_search_fields)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, genre_sort_fields)
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_genre_by_id(self, genre_id: int):
        return fetch_by_id(self.db, Genre, genre_id, "Genre not found")

    def create_genre(self, genre_data: CreateGenreSchema):
        genre = Genre(**genre_data.model_dump())
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def update_genre(self, genre_id: int, genre_data: UpdateGenreSchema):
        genre = self.get_genre_by_id(genre_id)
        updated_data = genre_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(genre, field, value)

        self.db.commit()
        self.db.refresh(genre)
        return genre

    def remove_genre(self, genre_id: int):
        genre = self.get_genre_by_id(genre_id)
        self.db.delete(genre)
        self.db.commit()

    def get_books_of_genre(
        self,
        genre_id: int,
        filters: dict,
        sorting_params: BookSortingSchema,
        pagination: PaginationParams,
    ):
        self.get_genre_by_id(genre_id)
        stmt = (
            select(Book)
            .join(BookGenre, Book.id == BookGenre.book_id)
            .where(BookGenre.genre_id == genre_id)
        )
        if any(filters):
            stmt = apply_filters(stmt, filters, book_search_fields)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, book_sort_fields)
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_genre_book_association(self, genre_id: int, book_id: int):
        self.get_genre_by_id(genre_id)
        fetch_by_id(self.db, Book, book_id, "Book not found")
        ensure_association_does_not_exist(
            self.db, BookGenre, genre_id=genre_id, book_id=book_id
        )
        self.db.add(BookGenre(genre_id=genre_id, book_id=book_id))
        self.db.commit()

    def remove_genre_book_association(self, genre_id: int, book_id: int):
        self.get_genre_by_id(genre_id)
        fetch_by_id(self.db, Book, book_id, "Book not found")
        association = fetch_association(
            self.db,
            BookGenre,
            "Association not found",
            genre_id=genre_id,
            book_id=book_id,
        )
        self.db.delete(association)
        self.db.commit()
