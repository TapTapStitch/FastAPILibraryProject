from fastapi import APIRouter, Depends, Response
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.book import BookSchema, CreateBookSchema, UpdateBookSchema
from ..schemas.author import AuthorSchema
from ..schemas.pagination import PaginationParams, PaginatedResponse
from ..crud.books import BooksCrud

router = APIRouter()


def get_books_crud(db: Session = Depends(get_db)) -> BooksCrud:
    return BooksCrud(db)


@router.get(
    "/",
    response_model=PaginatedResponse[BookSchema],
)
async def get_books(
    pagination: PaginationParams = Depends(), crud: BooksCrud = Depends(get_books_crud)
):
    return crud.get_books(pagination=pagination)


@router.get(
    "/{book_id}",
    response_model=BookSchema,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        }
                    }
                }
            },
        },
    },
)
async def get_book(book_id: int, crud: BooksCrud = Depends(get_books_crud)):
    return crud.get_book_by_id(book_id=book_id)


@router.post(
    "/",
    response_model=BookSchema,
    status_code=201,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {"example": {"detail": "ISBN must be unique"}}
            },
        }
    },
)
async def create_book_service(
    book: CreateBookSchema, crud: BooksCrud = Depends(get_books_crud)
):
    return crud.create_book(book_data=book)


@router.patch(
    "/{book_id}",
    response_model=BookSchema,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {"example": {"detail": "ISBN must be unique"}}
            },
        },
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        }
                    }
                }
            },
        },
    },
)
async def update_book(
    book_id: int, book: UpdateBookSchema, crud: BooksCrud = Depends(get_books_crud)
):
    return crud.update_book(
        book_id=book_id,
        book_data=book,
    )


@router.delete(
    "/{book_id}",
    status_code=204,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        }
                    }
                }
            },
        },
    },
)
async def delete_book(book_id: int, crud: BooksCrud = Depends(get_books_crud)):
    crud.remove_book(book_id=book_id)
    return Response(status_code=204)


@router.get(
    "/{book_id}/authors",
    response_model=PaginatedResponse[AuthorSchema],
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        }
                    }
                }
            },
        },
    },
)
def get_authors_of_book(
    book_id: int,
    pagination: PaginationParams = Depends(),
    crud: BooksCrud = Depends(get_books_crud),
):
    return crud.get_authors_of_book(book_id=book_id, pagination=pagination)


@router.post(
    "/{book_id}/authors/{author_id}",
    status_code=201,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        },
                        "author_not_found": {
                            "summary": "Author not found",
                            "value": {"detail": "Author not found"},
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
def create_book_author_association(
    book_id: int, author_id: int, crud: BooksCrud = Depends(get_books_crud)
):
    crud.create_book_author_association(book_id=book_id, author_id=author_id)
    return Response(status_code=201)


@router.delete(
    "/{book_id}/authors/{author_id}",
    status_code=204,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "book_not_found": {
                            "summary": "Book not found",
                            "value": {"detail": "Book not found"},
                        },
                        "author_not_found": {
                            "summary": "Author not found",
                            "value": {"detail": "Author not found"},
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
    book_id: int, author_id: int, crud: BooksCrud = Depends(get_books_crud)
):
    crud.remove_book_author_association(book_id=book_id, author_id=author_id)
    return Response(status_code=204)
