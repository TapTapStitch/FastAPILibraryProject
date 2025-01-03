import pytest
from pydantic import ValidationError
from typing import List
from app.schemas.pagination import PaginationParams, PaginatedResponse


def test_pagination_params_valid():
    params = PaginationParams(page=2, size=25)
    assert params.page == 2
    assert params.size == 25


def test_pagination_params_default():
    params = PaginationParams()
    assert params.page == 1
    assert params.size == 50


def test_pagination_params_invalid_page():
    with pytest.raises(ValidationError) as exc_info:
        PaginationParams(page=0, size=25)
    assert "greater than 0" in str(exc_info.value)


def test_pagination_params_invalid_size():
    with pytest.raises(ValidationError) as exc_info:
        PaginationParams(page=1, size=0)
    assert "greater than 0" in str(exc_info.value)


def test_paginated_response():
    items = ["item1", "item2", "item3"]
    total = 3
    page = 1
    size = 2
    pages = 2

    response = PaginatedResponse[str](
        items=items, total=total, page=page, size=size, pages=pages
    )

    assert response.items == items
    assert response.total == total
    assert response.page == page
    assert response.size == size
    assert response.pages == pages


def test_paginated_response_empty_items():
    items: List[str] = []
    total = 0
    page = 1
    size = 10
    pages = 0

    response = PaginatedResponse[str](
        items=items, total=total, page=page, size=size, pages=pages
    )

    assert response.items == items
    assert response.total == total
    assert response.page == page
    assert response.size == size
    assert response.pages == pages
