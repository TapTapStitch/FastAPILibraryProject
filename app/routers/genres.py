from fastapi import APIRouter, Depends, Response
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.genre import GenreSchema, CreateGenreSchema, UpdateGenreSchema
from ..schemas.book import BookSchema
from ..schemas.pagination import PaginationParams, PaginatedResponse
from ..crud.genres import GenresCrud

router = APIRouter()


def get_genres_crud(db: Session = Depends(get_db)) -> GenresCrud:
    return GenresCrud(db)


@router.get("/", response_model=PaginatedResponse[GenreSchema])
async def get_genres(
    pagination: PaginationParams = Depends(),
    crud: GenresCrud = Depends(get_genres_crud),
):
    return crud.get_genres(pagination=pagination)


@router.get(
    "/{genre_id}",
    response_model=GenreSchema,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
                        }
                    }
                }
            },
        },
    },
)
async def get_genre(genre_id: int, crud: GenresCrud = Depends(get_genres_crud)):
    return crud.get_genre_by_id(genre_id=genre_id)


@router.post("/", response_model=GenreSchema, status_code=201)
async def create_genre(
    genre: CreateGenreSchema, crud: GenresCrud = Depends(get_genres_crud)
):
    return crud.create_genre(genre_data=genre)


@router.patch(
    "/{genre_id}",
    response_model=GenreSchema,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
                        },
                    }
                }
            },
        },
    },
)
async def update_genre(
    genre_id: int,
    genre: UpdateGenreSchema,
    crud: GenresCrud = Depends(get_genres_crud),
):
    return crud.update_genre(
        genre_id=genre_id,
        genre_data=genre,
    )


@router.delete(
    "/{genre_id}",
    status_code=204,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
                        }
                    }
                }
            },
        },
    },
)
async def delete_genre(genre_id: int, crud: GenresCrud = Depends(get_genres_crud)):
    return crud.remove_genre(genre_id=genre_id)


@router.get(
    "/{genre_id}/books",
    response_model=PaginatedResponse[BookSchema],
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
                        }
                    }
                }
            },
        },
    },
)
def get_books_of_genre(
    genre_id: int,
    pagination: PaginationParams = Depends(),
    crud: GenresCrud = Depends(get_genres_crud),
):
    return crud.get_books_of_genre(genre_id=genre_id, pagination=pagination)


@router.post(
    "/{genre_id}/books/{book_id}",
    status_code=201,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
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
def create_genre_book_association(
    genre_id: int, book_id: int, crud: GenresCrud = Depends(get_genres_crud)
):
    crud.create_genre_book_association(genre_id=genre_id, book_id=book_id)
    return Response(status_code=201)


@router.delete(
    "/{genre_id}/books/{book_id}",
    status_code=204,
    responses={
        404: {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "genre_not_found": {
                            "summary": "Genre not found",
                            "value": {"detail": "Genre not found"},
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
async def delete_genre_book_association(
    genre_id: int, book_id: int, crud: GenresCrud = Depends(get_genres_crud)
):
    crud.remove_genre_book_association(genre_id=genre_id, book_id=book_id)
    return Response(status_code=204)
