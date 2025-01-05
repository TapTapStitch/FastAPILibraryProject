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
        return self._fetch_by_id(Author, author_id, "Author not found")

    def create_author(self, author_data: CreateAuthorSchema):
        author = Author(**author_data.model_dump())
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def update_author(self, author_id: int, author_data: UpdateAuthorSchema):
        author = self.get_author_by_id(author_id)
        updated_data = author_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(author, field, value)

        self.db.commit()
        self.db.refresh(author)
        return author

    def remove_author(self, author_id: int):
        author = self.get_author_by_id(author_id)
        self.db.delete(author)
        self.db.commit()

    def get_books_of_author(self, author_id: int, pagination: PaginationParams):
        self.get_author_by_id(author_id)
        stmt = (
            select(Book)
            .join(BookAuthor, Book.id == BookAuthor.book_id)
            .where(BookAuthor.author_id == author_id)
        )
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_author_book_association(self, author_id: int, book_id: int):
        self.get_author_by_id(author_id)
        self._fetch_by_id(Book, book_id, "Book not found")
        self._ensure_association_does_not_exist(
            BookAuthor, author_id=author_id, book_id=book_id
        )
        self.db.add(BookAuthor(author_id=author_id, book_id=book_id))
        self.db.commit()

    def remove_author_book_association(self, author_id: int, book_id: int):
        self.get_author_by_id(author_id)
        self._fetch_by_id(Book, book_id, "Book not found")
        association = self._fetch_association(
            BookAuthor, "Association not found", author_id=author_id, book_id=book_id
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
