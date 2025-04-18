from fastapi import APIRouter, Depends, Response
from app.schemas.api.v1.genre import (
    GenreSchema,
    CreateGenreSchema,
    UpdateGenreSchema,
    GenreSortingSchema,
    genre_search_dependency,
)
from app.schemas.api.v1.book import (
    BookSchema,
    BookSortingSchema,
    book_search_dependency,
)
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.crud.api.v1.genres import GenresCrud
from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    invalid_authentication_responses,
    filtering_validation_error_response,
    combine_responses,
)
from app.routers.api.v1.shared.depends import get_genres_crud, get_librarian_user

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[GenreSchema],
    responses=filtering_validation_error_response(),
)
async def get_genres(
    filters: dict = Depends(genre_search_dependency),
    sorting_params: GenreSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: GenresCrud = Depends(get_genres_crud),
):
    return crud.get_genres(
        filters=filters, sorting_params=sorting_params, pagination=pagination
    )


@router.get(
    "/{genre_id}", response_model=GenreSchema, responses=not_found_response("genre")
)
async def get_genre(genre_id: int, crud: GenresCrud = Depends(get_genres_crud)):
    return crud.get_genre_by_id(genre_id=genre_id)


@router.post(
    "/",
    response_model=GenreSchema,
    status_code=201,
    responses=invalid_authentication_responses(),
)
async def create_genre(
    genre: CreateGenreSchema,
    crud: GenresCrud = Depends(get_genres_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.create_genre(genre_data=genre)


@router.patch(
    "/{genre_id}",
    response_model=GenreSchema,
    responses=combine_responses(
        not_found_response("genre"), invalid_authentication_responses()
    ),
)
async def update_genre(
    genre_id: int,
    genre: UpdateGenreSchema,
    crud: GenresCrud = Depends(get_genres_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.update_genre(genre_id=genre_id, genre_data=genre)


@router.delete(
    "/{genre_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("genre"), invalid_authentication_responses()
    ),
)
async def delete_genre(
    genre_id: int,
    crud: GenresCrud = Depends(get_genres_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_genre(genre_id=genre_id)
    return Response(status_code=204)


@router.get(
    "/{genre_id}/books",
    response_model=PaginatedResponse[BookSchema],
    responses=combine_responses(
        not_found_response("genre"), filtering_validation_error_response()
    ),
)
def get_books_of_genre(
    genre_id: int,
    filters: dict = Depends(book_search_dependency),
    sorting_params: BookSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: GenresCrud = Depends(get_genres_crud),
):
    return crud.get_books_of_genre(
        genre_id=genre_id,
        filters=filters,
        sorting_params=sorting_params,
        pagination=pagination,
    )


@router.post(
    "/{genre_id}/books/{book_id}",
    status_code=201,
    responses=combine_responses(
        not_found_response("genre"),
        not_found_response("book"),
        bad_request_response("Association already exists"),
        invalid_authentication_responses(),
    ),
)
def create_genre_book_association(
    genre_id: int,
    book_id: int,
    crud: GenresCrud = Depends(get_genres_crud),
    current_user=Depends(get_librarian_user),
):
    crud.create_genre_book_association(genre_id=genre_id, book_id=book_id)
    return Response(status_code=201)


@router.delete(
    "/{genre_id}/books/{book_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("genre"),
        not_found_response("book"),
        not_found_response("association"),
        invalid_authentication_responses(),
    ),
)
async def delete_genre_book_association(
    genre_id: int,
    book_id: int,
    crud: GenresCrud = Depends(get_genres_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_genre_book_association(genre_id=genre_id, book_id=book_id)
    return Response(status_code=204)
