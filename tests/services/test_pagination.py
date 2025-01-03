import pytest
from sqlalchemy import select, desc
from app.models.book import Book
from app.schemas.pagination import PaginationParams
from app.services.pagination import paginate


@pytest.fixture()
def seed_books(session):
    books = [
        Book(
            title="Book 1",
            description="Description 1",
            year_of_publication=2021,
            isbn="ISBN001",
        ),
        Book(
            title="Book 2",
            description="Description 2",
            year_of_publication=2022,
            isbn="ISBN002",
        ),
        Book(
            title="Book 3",
            description="Description 3",
            year_of_publication=2023,
            isbn="ISBN003",
        ),
    ]
    session.add_all(books)
    session.commit()


def test_paginate(session, seed_books):
    stmt = select(Book).order_by(desc(Book.created_at))

    # Test pagination with page=1 and size=2
    pagination_params = PaginationParams(page=1, size=2)
    response = paginate(session, stmt, pagination_params)

    assert response.page == 1
    assert response.size == 2
    assert response.total == 3
    assert response.pages == 2
    assert len(response.items) == 2
    assert response.items[0].title == "Book 1"
    assert response.items[1].title == "Book 2"

    # Test pagination with page=2 and size=2
    pagination_params = PaginationParams(page=2, size=2)
    response = paginate(session, stmt, pagination_params)

    assert response.page == 2
    assert response.size == 2
    assert response.total == 3
    assert response.pages == 2
    assert len(response.items) == 1
    assert response.items[0].title == "Book 3"

    # Test pagination with page exceeding available data
    pagination_params = PaginationParams(page=3, size=2)
    response = paginate(session, stmt, pagination_params)

    assert response.page == 3
    assert response.size == 2
    assert response.total == 3
    assert response.pages == 2
    assert len(response.items) == 0
