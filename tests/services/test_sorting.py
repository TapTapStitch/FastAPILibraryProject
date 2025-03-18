import pytest
from sqlalchemy import select, asc, desc
from app.models.book import Book
from app.services.sorting import apply_sorting
from app.schemas.api.v1.book import BookSortingSchema


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


def test_apply_sorting_asc(session, seed_books):
    stmt = select(Book)
    sort_fields = {
        "title": Book.title,
        "created_at": Book.created_at,
    }
    sorting_params = BookSortingSchema(sort_by="title", sort_order="asc")
    stmt_sorted = apply_sorting(stmt, sorting_params, sort_fields)
    results = session.execute(stmt_sorted).scalars().all()
    titles = [book.title for book in results]
    assert titles == ["Book 1", "Book 2", "Book 3"]


def test_apply_sorting_desc(session, seed_books):
    stmt = select(Book)
    sort_fields = {
        "title": Book.title,
        "created_at": Book.created_at,
    }
    sorting_params = BookSortingSchema(sort_by="title", sort_order="desc")
    stmt_sorted = apply_sorting(stmt, sorting_params, sort_fields)
    results = session.execute(stmt_sorted).scalars().all()
    titles = [book.title for book in results]
    assert titles == ["Book 3", "Book 2", "Book 1"]
