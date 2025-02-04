from fastapi import APIRouter, Depends, Response
from app.schemas.author import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
from app.schemas.book import BookSchema
from app.schemas.pagination import PaginationParams, PaginatedResponse
from app.crud.authors import AuthorsCrud
from app.routers.shared.response_templates import (
    not_found_response,
    bad_request_response,
    combine_responses,
)
from app.routers.shared.depends import get_authors_crud

router = APIRouter()


@router.get("/", response_model=PaginatedResponse[AuthorSchema])
async def get_authors(
    pagination: PaginationParams = Depends(),
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.get_authors(pagination=pagination)


@router.get(
    "/{author_id}", response_model=AuthorSchema, responses=not_found_response("author")
)
async def get_author(author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)):
    return crud.get_author_by_id(author_id=author_id)


@router.post("/", response_model=AuthorSchema, status_code=201)
async def create_author(
    author: CreateAuthorSchema, crud: AuthorsCrud = Depends(get_authors_crud)
):
    return crud.create_author(author_data=author)


@router.patch(
    "/{author_id}", response_model=AuthorSchema, responses=not_found_response("author")
)
async def update_author(
    author_id: int,
    author: UpdateAuthorSchema,
    crud: AuthorsCrud = Depends(get_authors_crud),
):
    return crud.update_author(author_id=author_id, author_data=author)


@router.delete("/{author_id}", status_code=204, responses=not_found_response("author"))
async def delete_author(author_id: int, crud: AuthorsCrud = Depends(get_authors_crud)):
    crud.remove_author(author_id=author_id)
    return Response(status_code=204)


@router.get(
    "/{author_id}/books",
    response_model=PaginatedResponse[BookSchema],
    responses=not_found_response("author"),
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
    responses=combine_responses(
        not_found_response("author"),
        not_found_response("book"),
        bad_request_response("Association already exists"),
    ),
)
def create_author_book_association(
    author_id: int, book_id: int, crud: AuthorsCrud = Depends(get_authors_crud)
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
    ),
)
async def delete_author_book_association(
    author_id: int, book_id: int, crud: AuthorsCrud = Depends(get_authors_crud)
):
    crud.remove_author_book_association(author_id=author_id, book_id=book_id)
    return Response(status_code=204)
