from sqlalchemy.orm import Session
from sqlalchemy import select
from app.services.pagination import paginate
from app.models.book import Book
from app.models.author import Author
from app.models.book_author import BookAuthor
from app.schemas.api.v1.author import (
    CreateAuthorSchema,
    UpdateAuthorSchema,
    AuthorSortingSchema,
)
from app.schemas.api.v1.book import BookSortingSchema
from app.schemas.pagination import PaginationParams
from app.services.sorting import apply_sorting
from app.crud.shared.db_utils import (
    fetch_by_id,
    ensure_association_does_not_exist,
    fetch_association,
)
from app.crud.api.v1.shared.sort_fields import book_sort_fields, author_sort_fields


class AuthorsCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_authors(
        self, pagination: PaginationParams, sorting_params: AuthorSortingSchema
    ):
        stmt = select(Author)
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, author_sort_fields)
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_author_by_id(self, author_id: int):
        return fetch_by_id(self.db, Author, author_id, "Author not found")

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

    def get_books_of_author(
        self,
        author_id: int,
        pagination: PaginationParams,
        sorting_params: BookSortingSchema,
    ):
        self.get_author_by_id(author_id)
        stmt = (
            select(Book)
            .join(BookAuthor, Book.id == BookAuthor.book_id)
            .where(BookAuthor.author_id == author_id)
        )
        if sorting_params.sort_by:
            stmt = apply_sorting(stmt, sorting_params, book_sort_fields)
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def create_author_book_association(self, author_id: int, book_id: int):
        self.get_author_by_id(author_id)
        fetch_by_id(self.db, Book, book_id, "Book not found")
        ensure_association_does_not_exist(
            self.db, BookAuthor, author_id=author_id, book_id=book_id
        )
        self.db.add(BookAuthor(author_id=author_id, book_id=book_id))
        self.db.commit()

    def remove_author_book_association(self, author_id: int, book_id: int):
        self.get_author_by_id(author_id)
        fetch_by_id(self.db, Book, book_id, "Book not found")
        association = fetch_association(
            self.db,
            BookAuthor,
            "Association not found",
            author_id=author_id,
            book_id=book_id,
        )
        self.db.delete(association)
        self.db.commit()
