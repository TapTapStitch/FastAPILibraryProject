from typing import TypeVar, Generic, Sequence
from pydantic import BaseModel
from fastapi import Query

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Query(
        1, gt=0, description="Page number, default is 1, must be greater than 0"
    )
    size: int = Query(
        50, gt=0, description="Page size, default is 50, must be greater than 0"
    )


class PaginatedResponse(BaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    page: int
    size: int
    pages: int
