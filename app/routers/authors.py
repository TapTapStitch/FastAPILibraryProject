from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.author import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from ..crud.authors import AuthorsCrud

router = APIRouter()
crud = AuthorsCrud()


@router.get("/", response_model=Page[AuthorSchema])
async def get_authors(db: Session = Depends(get_db)):
    return crud.get_authors(db)


@router.get(
    "/{author_id}",
    response_model=AuthorSchema,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "author_not_found": {
                            "summary": "Author not found",
                            "value": {"detail": "Author not found"},
                        }
                    }
                }
            },
        },
    },
)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    return crud.get_author_by_id(db, author_id=author_id)


@router.post(
    "/",
    response_model=AuthorSchema,
    status_code=201,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "example": {"detail": "One or more books not found"}
                }
            },
        },
    },
)
async def create_author_service(
    author: CreateAuthorSchema, db: Session = Depends(get_db)
):
    return crud.create_author(db, author_data=author)


@router.patch(
    "/{author_id}",
    response_model=AuthorSchema,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "author_not_found": {
                            "summary": "Author not found",
                            "value": {"detail": "Author not found"},
                        },
                        "books_not_found": {
                            "summary": "One or more books not found",
                            "value": {"detail": "One or more books not found"},
                        },
                    }
                }
            },
        },
    },
)
async def update_author(
    author_id: int, author: UpdateAuthorSchema, db: Session = Depends(get_db)
):
    return crud.update_author(
        db,
        author_id=author_id,
        author_data=author,
    )


@router.delete(
    "/{author_id}",
    status_code=204,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "author_not_found": {
                            "summary": "Author not found",
                            "value": {"detail": "Author not found"},
                        }
                    }
                }
            },
        },
    },
)
async def delete_author(author_id: int, db: Session = Depends(get_db)):
    return crud.remove_author(db, author_id=author_id)
