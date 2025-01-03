from fastapi import APIRouter, Depends
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.book import BookSchema, CreateBookSchema, UpdateBookSchema
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
    return crud.remove_book(book_id=book_id)
