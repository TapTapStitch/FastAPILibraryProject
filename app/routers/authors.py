from fastapi import APIRouter, Depends
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.author import AuthorSchema, CreateAuthorSchema, UpdateAuthorSchema
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
