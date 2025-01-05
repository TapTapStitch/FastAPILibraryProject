from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.genre import Genre
from ..models.book import Book
from ..models.book_genre import BookGenre
from ..schemas.genre import CreateGenreSchema, UpdateGenreSchema
from ..schemas.pagination import PaginationParams


class GenresCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_genres(self, pagination: PaginationParams):
        stmt = select(Genre).order_by(desc(Genre.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_genre_by_id(self, genre_id: int):
        return self._fetch_genre_by_id(genre_id)

    def create_genre(self, genre_data: CreateGenreSchema):
        genre = Genre(name=genre_data.name, description=genre_data.description)
        self.db.add(genre)
        self.db.commit()
        self.db.refresh(genre)
        return genre

    def update_genre(self, genre_id: int, genre_data: UpdateGenreSchema):
        genre = self._fetch_genre_by_id(genre_id)
        updated_data = genre_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(genre, field, value)

        self.db.commit()
        self.db.refresh(genre)
        return genre

    def remove_genre(self, genre_id: int):
        genre = self._fetch_genre_by_id(genre_id)
        self.db.delete(genre)
        self.db.commit()

    def get_books_of_genre(self, genre_id: int, pagination: PaginationParams):
        self._fetch_genre_by_id(genre_id)
        stmt = (
            select(Book)
            .join(BookGenre, Book.id == BookGenre.book_id)
            .where(BookGenre.genre_id == genre_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_genre_book_association(self, genre_id: int, book_id: int):
        self._fetch_genre_by_id(genre_id)
        self._ensure_book_exists(book_id)
        self._ensure_association_does_not_exist(genre_id, book_id)
        book_genre = BookGenre(genre_id=genre_id, book_id=book_id)
        self.db.add(book_genre)
        self.db.commit()

    def remove_genre_book_association(self, genre_id: int, book_id: int):
        self._fetch_genre_by_id(genre_id)
        self._ensure_book_exists(book_id)
        association = self._fetch_association(genre_id, book_id)
        if not association:
            raise HTTPException(status_code=404, detail="Association not found")
        self.db.delete(association)
        self.db.commit()

    def _fetch_genre_by_id(self, genre_id: int):
        genre = self.db.execute(
            select(Genre).where(Genre.id == genre_id)
        ).scalar_one_or_none()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre not found")
        return genre

    def _ensure_book_exists(self, book_id: int):
        if not self.db.execute(
            select(Book).where(Book.id == book_id)
        ).scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Book not found")

    def _ensure_association_does_not_exist(self, genre_id: int, book_id: int):
        association_exists = self.db.execute(
            select(BookGenre).filter_by(genre_id=genre_id, book_id=book_id)
        ).scalar_one_or_none()
        if association_exists:
            raise HTTPException(
                status_code=400,
                detail="Association already exists",
            )

    def _fetch_association(self, genre_id: int, book_id: int):
        return self.db.execute(
            select(BookGenre).filter_by(genre_id=genre_id, book_id=book_id)
        ).scalar_one_or_none()
