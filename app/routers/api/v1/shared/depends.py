from fastapi import Depends
from sqlalchemy.orm import Session
from app.config import get_db
from app.crud.api.v1.books import BooksCrud
from app.crud.api.v1.authors import AuthorsCrud
from app.crud.api.v1.genres import GenresCrud
from app.crud.api.v1.users import UsersCrud
from app.services.authorization import get_current_user_with_minimum_role, Role


def get_books_crud(db: Session = Depends(get_db)) -> BooksCrud:
    return BooksCrud(db)


def get_authors_crud(db: Session = Depends(get_db)) -> AuthorsCrud:
    return AuthorsCrud(db)


def get_genres_crud(db: Session = Depends(get_db)) -> GenresCrud:
    return GenresCrud(db)


def get_users_crud(db: Session = Depends(get_db)) -> UsersCrud:
    return UsersCrud(db)


get_librarian_user = get_current_user_with_minimum_role(Role.LIBRARIAN)
get_admin_user = get_current_user_with_minimum_role(Role.ADMIN)
