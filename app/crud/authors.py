from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc
from fastapi import HTTPException
from ..models.author import Author
from ..models.book import Book
from ..schemas.author import ChangeAuthorSchema


class AuthorsCrud:
    def get_authors(self, db: Session):
        return db.query(Author).options(selectinload(Author.books)).order_by(desc(Author.created_at))

    def get_author_by_id(self, db: Session, author_id: int):
        author = db.query(Author).options(selectinload(Author.books)).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def create_author(self, db: Session, author_data: ChangeAuthorSchema):
        books = db.query(Book).filter(Author.id.in_(author_data.books)).all()

        if len(books) != len(author_data.books):
            raise HTTPException(status_code=404, detail="One or more books not found")

        author = Author(
            name=author_data.name,
            surname=author_data.surname,
            year_of_birth=author_data.year_of_birth,
            biography=author_data.biography,
            books=books,
        )
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    def update_author(
        self, db: Session, author_id: int, author_data: ChangeAuthorSchema
    ):
        author = self.get_author_by_id(db=db, author_id=author_id)
        updated_data = author_data.model_dump(exclude_unset=True)

        books = db.query(Book).filter(Author.id.in_(author_data.books)).all()

        if len(books) != len(author_data.books):
            raise HTTPException(status_code=404, detail="One or more books not found")

        updated_data["books"] = books

        for field, value in updated_data.items():
            setattr(author, field, value)
        db.commit()
        db.refresh(author)
        return author

    def remove_author(self, db: Session, author_id: int):
        author = self.get_author_by_id(db=db, author_id=author_id)
        db.delete(author)
        db.commit()
