from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from app.services.pagination import paginate
from app.models.genre import Genre
from app.models.book import Book
from app.models.book_genre import BookGenre
from app.schemas.api.v1.genre import CreateGenreSchema, UpdateGenreSchema
from app.schemas.pagination import PaginationParams
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_association_does_not_exist,
    fetch_association,
)


class GenresCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_genres(self, pagination: PaginationParams):
        stmt = select(Genre).order_by(desc(Genre.created_at))
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

    def get_books_of_genre(self, genre_id: int, pagination: PaginationParams):
        self.get_genre_by_id(genre_id)
        stmt = (
            select(Book)
            .join(BookGenre, Book.id == BookGenre.book_id)
            .where(BookGenre.genre_id == genre_id)
        )
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
