from sqlalchemy.orm import Session, selectinload
from sqlalchemy import desc, select
from fastapi import HTTPException
from ..services.pagination import paginate
from ..models.author import Author
from ..schemas.author import CreateAuthorSchema, UpdateAuthorSchema


class AuthorsCrud:
    def __init__(self, db: Session):
        self.db = db

    def get_authors(self, pagination):
        stmt = select(Author).order_by(desc(Author.created_at))
        return paginate(self.db, stmt=stmt, pagination=pagination)

    def get_author_by_id(self, author_id: int):
        author = self._get_author_by_id(author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Author not found")
        return author

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
        author = self.get_author_by_id(author_id=author_id)
        updated_data = author_data.model_dump(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(author, field, value)

        self.db.commit()
        self.db.refresh(author)
        return author

    def remove_author(self, author_id: int):
        author = self.get_author_by_id(author_id=author_id)
        self.db.delete(author)
        self.db.commit()

    def _get_author_by_id(self, author_id: int):
        return self.db.execute(
            select(Author).where(Author.id == author_id)
        ).scalar_one_or_none()
