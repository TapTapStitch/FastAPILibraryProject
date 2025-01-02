from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc
from fastapi import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from ..models.author import Author
from ..models.book import Book
from ..schemas.author import CreateAuthorSchema, UpdateAuthorSchema


class AuthorsCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_authors(self):
        authors = (
            self.db.query(Author)
            .options(selectinload(Author.books))
            .order_by(desc(Author.created_at))
        )
        return paginate(authors)

    def get_author_by_id(self, author_id: int):
        author = self.db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def create_author(self, author_data: CreateAuthorSchema):
        books = self.db.query(Book).filter(Book.id.in_(author_data.books)).all()

        if len(books) != len(author_data.books):
            raise HTTPException(status_code=404, detail="One or more books not found")

        author = Author(
            name=author_data.name,
            surname=author_data.surname,
            year_of_birth=author_data.year_of_birth,
            biography=author_data.biography,
            books=books,
        )
        self.db.add(author)
        self.db.commit()
        self.db.refresh(author)
        return author

    def update_author(self, author_id: int, author_data: UpdateAuthorSchema):
        author = self.get_author_by_id(author_id=author_id)
        updated_data = author_data.model_dump(exclude_unset=True)

        if "books" in updated_data:
            books = self.db.query(Book).filter(Book.id.in_(author_data.books)).all()
            if len(books) != len(author_data.books):
                raise HTTPException(
                    status_code=404, detail="One or more books not found"
                )
            updated_data["books"] = books

        for field, value in updated_data.items():
            setattr(author, field, value)

        self.db.commit()
        self.db.refresh(author)
        return author

    def remove_author(self, author_id: int):
        author = self.get_author_by_id(author_id=author_id)
        self.db.delete(author)
        self.db.commit()