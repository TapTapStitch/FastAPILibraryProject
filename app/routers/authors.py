from fastapi import APIRouter, Depends, Response
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.author import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from ..schemas.book import BookSchema
from ..schemas.pagination import PaginationParams, PaginatedResponse
from ..crud.authors import AuthorsCrud

router = APIRouter()


def get_authors_crud(db: Session = Depends(get_db)) -> AuthorsCrud:
    return AuthorsCrud(db)


@router.get("/", response_model=PaginatedResponse[AuthorSchema])
async def get_authors(
    pagination: PaginationParams = Depends(),
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.get_authors(pagination=pagination)


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
async def get_author(author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)):
    return crud.get_author_by_id(author_id=author_id)


@router.post("/", response_model=AuthorSchema, status_code=201)
async def create_author_service(
    author: CreateAuthorSchema, crud: AuthorsCrud = Depends(get_authors_crud)
):
    return crud.create_author(author_data=author)


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
                    }
                }
            },
        },
    },
)
async def update_author(
    author_id: int,
    author: UpdateAuthorSchema,
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.update_author(
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
async def delete_author(author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)):
    return crud.remove_author(author_id=author_id)


@router.get(
    "/{author_id}/books",
    response_model=PaginatedResponse[BookSchema],
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
def get_books_of_author(
    author_id: int,
    pagination: PaginationParams = Depends(),
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.get_books_of_author(author_id=author_id, pagination=pagination)


@router.post(
    "/{author_id}/books/{book_id}",
    status_code=201,
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
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        },
                    }
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "association_exists": {
                            "summary": "Association exists",
                            "value": {"detail": "Association already exists"},
                        }
                    }
                }
            },
        },
    },
)
def create_author_book_association(
    author_id: int, book_id: int, crud: AuthorsCrud = Depends(get_authors_crud)
):
    crud.create_author_book_association(author_id=author_id, book_id=book_id)
    return Response(status_code=201)


@router.delete(
    "/{author_id}/books/{book_id}",
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
                        },
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        },
                        "association_not_found": {
                            "summary": "Association not found",
                            "value": {"detail": "Association not found"},
                        },
                    }
                }
            },
        },
    },
)
async def delete_book_author_association(
    book_id: int, author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)
):
    crud.remove_author_book_association(author_id=author_id, book_id=book_id)
    return Response(status_code=204)
