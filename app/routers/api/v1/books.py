from fastapi import APIRouter, Depends, Response
from app.schemas.api.v1.book import (
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
    BookSortingSchema,
    book_search_dependency,
)
from app.schemas.api.v1.author import (
    AuthorSchema,
    AuthorSortingSchema,
    author_search_dependency,
)
from app.schemas.api.v1.genre import (
    GenreSchema,
    GenreSortingSchema,
    genre_search_dependency,
)
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.crud.api.v1.books import BooksCrud
from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    invalid_authentication_responses,
    filtering_validation_error_response,
    combine_responses,
)
from app.routers.api.v1.shared.depends import get_books_crud, get_librarian_user

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[BookSchema],
    responses=filtering_validation_error_response(),
)
async def get_books(
    filters: dict = Depends(book_search_dependency),
    sorting_params: BookSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: BooksCrud = Depends(get_books_crud),
):
    return crud.get_books(
        filters=filters,
        sorting_params=sorting_params,
        pagination=pagination,
    )


@router.get(
    "/{book_id}", response_model=BookSchema, responses=not_found_response("book")
)
async def get_book(book_id: int, crud: BooksCrud = Depends(get_books_crud)):
    return crud.get_book_by_id(book_id=book_id)


@router.post(
    "/",
    response_model=BookSchema,
    status_code=201,
    responses=combine_responses(
        bad_request_response("ISBN must be unique"), invalid_authentication_responses()
    ),
)
async def create_book(
    book: CreateBookSchema,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.create_book(book_data=book)


@router.patch(
    "/{book_id}",
    response_model=BookSchema,
    responses=combine_responses(
        bad_request_response("ISBN must be unique"),
        not_found_response("book"),
        invalid_authentication_responses(),
    ),
)
async def update_book(
    book_id: int,
    book: UpdateBookSchema,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.update_book(book_id=book_id, book_data=book)


@router.delete(
    "/{book_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("book"), invalid_authentication_responses()
    ),
)
async def delete_book(
    book_id: int,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_book(book_id=book_id)
    return Response(status_code=204)


@router.get(
    "/{book_id}/authors",
    response_model=PaginatedResponse[AuthorSchema],
    responses=combine_responses(
        not_found_response("book"), filtering_validation_error_response()
    ),
)
def get_authors_of_book(
    book_id: int,
    filters: dict = Depends(author_search_dependency),
    sorting_params: AuthorSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: BooksCrud = Depends(get_books_crud),
):
    return crud.get_authors_of_book(
        book_id=book_id,
        filters=filters,
        sorting_params=sorting_params,
        pagination=pagination,
    )


@router.post(
    "/{book_id}/authors/{author_id}",
    status_code=201,
    responses=combine_responses(
        not_found_response("book"),
        not_found_response("author"),
        bad_request_response("Association already exists"),
        invalid_authentication_responses(),
    ),
)
def create_book_author_association(
    book_id: int,
    author_id: int,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    crud.create_book_author_association(book_id=book_id, author_id=author_id)
    return Response(status_code=201)


@router.delete(
    "/{book_id}/authors/{author_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("book"),
        not_found_response("author"),
        not_found_response("association"),
        invalid_authentication_responses(),
    ),
)
async def delete_book_author_association(
    book_id: int,
    author_id: int,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_book_author_association(book_id=book_id, author_id=author_id)
    return Response(status_code=204)


@router.get(
    "/{book_id}/genres",
    response_model=PaginatedResponse[GenreSchema],
    responses=combine_responses(
        not_found_response("book"), filtering_validation_error_response()
    ),
)
def get_genres_of_book(
    book_id: int,
    filters: dict = Depends(genre_search_dependency),
    sorting_params: GenreSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: BooksCrud = Depends(get_books_crud),
):
    return crud.get_genres_of_book(
        book_id=book_id,
        filters=filters,
        sorting_params=sorting_params,
        pagination=pagination,
    )


@router.post(
    "/{book_id}/genres/{genre_id}",
    status_code=201,
    responses=combine_responses(
        not_found_response("book"),
        not_found_response("genre"),
        bad_request_response("Association already exists"),
        invalid_authentication_responses(),
    ),
)
def create_book_genre_association(
    book_id: int,
    genre_id: int,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    crud.create_book_genre_association(book_id=book_id, genre_id=genre_id)
    return Response(status_code=201)


@router.delete(
    "/{book_id}/genres/{genre_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("book"),
        not_found_response("genre"),
        not_found_response("association"),
        invalid_authentication_responses(),
    ),
)
async def delete_book_genre_association(
    book_id: int,
    genre_id: int,
    crud: BooksCrud = Depends(get_books_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_book_genre_association(book_id=book_id, genre_id=genre_id)
    return Response(status_code=204)
