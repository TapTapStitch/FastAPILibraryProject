from sqlalchemy.orm import Session
from sqlalchemy import desc
from fastapi import HTTPException
from ..models.author import Author
from ..schemas.author import ChangeAuthorSchema


class AuthorsCrud:
    def get_authors(self, db: Session):
        return db.query(Author).order_by(desc(Author.created_at))

    def get_author_by_id(self, db: Session, author_id: int):
        author = db.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

    def create_author(self, db: Session, author_data: ChangeAuthorSchema):
        author = Author(**author_data.model_dump())
        db.add(author)
        db.commit()
        db.refresh(author)
        return author

    def update_author(
        self, db: Session, author_id: int, author_data: ChangeAuthorSchema
    ):
        author = self.get_author_by_id(db=db, author_id=author_id)
        for field, value in author_data.model_dump(exclude_unset=True).items():
            setattr(author, field, value)
        db.commit()
        db.refresh(author)
        return author

    def remove_author(self, db: Session, author_id: int):
        author = self.get_author_by_id(db=db, author_id=author_id)
        db.delete(author)
        db.commit()
