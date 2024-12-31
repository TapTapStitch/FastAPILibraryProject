from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.author import AuthorSchema, ChangeAuthorSchema
from ..crud.authors import AuthorsCrud

router = APIRouter()
crud = AuthorsCrud()


@router.get("/", response_model=Page[AuthorSchema])
async def get_authors(db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return paginate(authors)


@router.get(
    "/{author_id}",
    response_model=AuthorSchema,
    responses={404: {"detail": "Author not found"}},
)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author_by_id(db, author_id=author_id)
    return author


@router.post("/", response_model=AuthorSchema, status_code=201)
async def create_author_service(
    author: ChangeAuthorSchema, db: Session = Depends(get_db)
):
    author = crud.create_author(db, author_data=author)
    return author


@router.patch(
    "/{author_id}",
    response_model=AuthorSchema,
    responses={404: {"detail": "Author not found"}},
)
async def update_author(
    author_id: int, author: ChangeAuthorSchema, db: Session = Depends(get_db)
):
    author = crud.update_author(
        db,
        author_id=author_id,
        author_data=author,
    )
    return author


@router.delete(
    "/{author_id}", status_code=204, responses={404: {"detail": "Author not found"}}
)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    crud.remove_author(db, author_id=author_id)
    return None
