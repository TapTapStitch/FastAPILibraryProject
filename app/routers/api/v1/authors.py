from fastapi import APIRouter, Depends, Response
from app.schemas.api.v1.author import (
    AuthorSchema,
    CreateAuthorSchema,
    UpdateAuthorSchema,
    AuthorSortingSchema,
    author_search_dependency,
)
from app.schemas.api.v1.book import (
    BookSchema,
    BookSortingSchema,
    book_search_dependency,
)
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.crud.api.v1.authors import AuthorsCrud
from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    invalid_authentication_responses,
    filtering_validation_error_response,
    combine_responses,
)
from app.routers.api.v1.shared.depends import get_authors_crud, get_librarian_user

router = APIRouter()


@router.get(
    "/",
    response_model=PaginatedResponse[AuthorSchema],
    responses=filtering_validation_error_response(),
)
async def get_authors(
    filters: dict = Depends(author_search_dependency),
    sorting_params: AuthorSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.get_authors(
        filters=filters, sorting_params=sorting_params, pagination=pagination
    )


@router.get(
    "/{author_id}", response_model=AuthorSchema, responses=not_found_response("author")
)
async def get_author(author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)):
    return crud.get_author_by_id(author_id=author_id)


@router.post(
    "/",
    response_model=AuthorSchema,
    status_code=201,
    responses=invalid_authentication_responses(),
)
async def create_author(
    author: CreateAuthorSchema,
    crud: AuthorsCrud = Depends(get_authors_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.create_author(author_data=author)


@router.patch(
    "/{author_id}",
    response_model=AuthorSchema,
    responses=combine_responses(
        not_found_response("author"), invalid_authentication_responses()
    ),
)
async def update_author(
    author_id: int,
    author: UpdateAuthorSchema,
    crud: AuthorsCrud = Depends(get_authors_crud),
    current_user=Depends(get_librarian_user),
):
    return crud.update_author(author_id=author_id, author_data=author)


@router.delete(
    "/{author_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("author"), invalid_authentication_responses()
    ),
)
async def delete_author(
    author_id: int,
    crud: AuthorsCrud = Depends(get_authors_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_author(author_id=author_id)
    return Response(status_code=204)


@router.get(
    "/{author_id}/books",
    response_model=PaginatedResponse[BookSchema],
    responses=combine_responses(
        not_found_response("author"), filtering_validation_error_response()
    ),
)
def get_books_of_author(
    author_id: int,
    filters: dict = Depends(book_search_dependency),
    sorting_params: BookSortingSchema = Depends(),
    pagination: PaginationParams = Depends(),
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.get_books_of_author(
        author_id=author_id,
        filters=filters,
        sorting_params=sorting_params,
        pagination=pagination,
    )


@router.post(
    "/{author_id}/books/{book_id}",
    status_code=201,
    responses=combine_responses(
        not_found_response("author"),
        not_found_response("book"),
        bad_request_response("Association already exists"),
        invalid_authentication_responses(),
    ),
)
def create_author_book_association(
    author_id: int,
    book_id: int,
    crud: AuthorsCrud = Depends(get_authors_crud),
    current_user=Depends(get_librarian_user),
):
    crud.create_author_book_association(author_id=author_id, book_id=book_id)
    return Response(status_code=201)


@router.delete(
    "/{author_id}/books/{book_id}",
    status_code=204,
    responses=combine_responses(
        not_found_response("author"),
        not_found_response("book"),
        not_found_response("association"),
        invalid_authentication_responses(),
    ),
)
async def delete_author_book_association(
    author_id: int,
    book_id: int,
    crud: AuthorsCrud = Depends(get_authors_crud),
    current_user=Depends(get_librarian_user),
):
    crud.remove_author_book_association(author_id=author_id, book_id=book_id)
    return Response(status_code=204)
