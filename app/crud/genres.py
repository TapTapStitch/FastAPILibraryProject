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
        return self._fetch_by_id(Genre, genre_id, "Genre not found")

    def create_genre(self, genre_data: CreateGenreSchema):
        genre = Genre(**genre_data.dict())
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
        self._fetch_by_id(Book, book_id, "Book not found")
        self._ensure_association_does_not_exist(
            BookGenre, genre_id=genre_id, book_id=book_id
        )
        self.db.add(BookGenre(genre_id=genre_id, book_id=book_id))
        self.db.commit()

    def remove_genre_book_association(self, genre_id: int, book_id: int):
        self.get_genre_by_id(genre_id)
        self._fetch_by_id(Book, book_id, "Book not found")
        association = self._fetch_association(
            BookGenre, "Association not found", genre_id=genre_id, book_id=book_id
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
