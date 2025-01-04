from sqlalchemy.orm import Session
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.book import Book
from ..models.author import Author
from ..models.book_author import BookAuthor
from ..schemas.author import CreateAuthorSchema, UpdateAuthorSchema
from ..schemas.pagination import PaginationParams


class AuthorsCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_authors(self, pagination: PaginationParams):
        stmt = select(Author).order_by(desc(Author.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_author_by_id(self, author_id: int):
        return self._fetch_author_by_id(author_id)

    def create_author(self, author_data: CreateAuthorSchema):
        author = Author(
            name=author_data.name,
            surname=author_data.surname,
            year_of_birth=author_data.year_of_birth,
            biography=author_data.biography,
        )
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def update_author(self, author_id: int, author_data: UpdateAuthorSchema):
        author = self._fetch_author_by_id(author_id)
        updated_data = author_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(author, field, value)

        self.db.commit()
        self.db.refresh(author)
        return author

    def remove_author(self, author_id: int):
        author = self._fetch_author_by_id(author_id)
        self.db.delete(author)
        self.db.commit()

    def get_books_of_author(self, author_id: int, pagination: PaginationParams):
        self._fetch_author_by_id(author_id)
        stmt = (
            select(Book)
            .join(BookAuthor, Book.id == BookAuthor.book_id)
            .where(BookAuthor.author_id == author_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_author_book_association(self, author_id: int, book_id: int):
        self._fetch_author_by_id(author_id)
        self._ensure_book_exists(book_id)
        self._ensure_association_does_not_exist(author_id, book_id)
        book_author = BookAuthor(author_id=author_id, book_id=book_id)
        self.db.add(book_author)
        self.db.commit()

    def remove_author_book_association(self, author_id: int, book_id: int):
        self._fetch_author_by_id(author_id)
        self._ensure_book_exists(book_id)
        association = self._fetch_association(author_id, book_id)
        if not association:
            raise HTTPException(status_code=404, detail="Association not found")
        self.db.delete(association)
        self.db.commit()

    def _fetch_author_by_id(self, author_id: int):
        author = self.db.execute(
            select(Author).where(Author.id == author_id)
        ).scalar_one_or_none()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def _ensure_book_exists(self, book_id: int):
        if not self.db.execute(
            select(Book).where(Book.id == book_id)
        ).scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Book not found")

    def _ensure_association_does_not_exist(self, author_id: int, book_id: int):
        association_exists = self.db.execute(
            select(BookAuthor).filter_by(author_id=author_id, book_id=book_id)
        ).scalar_one_or_none()
        if association_exists:
            raise HTTPException(
                status_code=400,
                detail="Association already exists",
            )

    def _fetch_association(self, author_id: int, book_id: int):
        return self.db.execute(
            select(BookAuthor).filter_by(author_id=author_id, book_id=book_id)
        ).scalar_one_or_none()
