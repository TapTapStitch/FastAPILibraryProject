from fastapi import APIRouter
from fastapi import Depends
from ..config import SessionLocal
from sqlalchemy.orm import Session
from ..schemas.base import Response
from ..schemas.book import (
    BookIndexSchema,
    BookShowSchema,
    BookCreateSchema,
    BookUpdateSchema,
)
from ..crud import book as crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[BookIndexSchema])
async def get_books(db: Session = Depends(get_db)):
    _books = crud.get_books(db)
    return Response(
        status="Ok", code="200", message="Success fetch all data", result=_books
    )


@router.get("/{book_id}", response_model=BookShowSchema)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    _book = crud.get_book_by_id(db, book_id=book_id)
    return Response(
        status="Ok", code="200", message="Success fetch all data", result=_book
    )


@router.post("/")
async def create_book_service(book: BookCreateSchema, db: Session = Depends(get_db)):
    _book = crud.create_book(db, title=book.title, description=book.description)
    return Response(
        status="Ok", code="200", message="Book created successfully", result=_book
    )


@router.patch("/{book_id}", response_model=BookShowSchema)
async def update_book(
    book_id: int, book: BookUpdateSchema, db: Session = Depends(get_db)
):
    _book = crud.update_book(
        db,
        book_id=book_id,
        title=book.title,
        description=book.description,
    )
    return Response(
        status="Ok", code="200", message="Success update book", result=_book
    )


@router.delete("/{book_id}")
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.remove_book(db, book_id=book_id)
    return Response(status="Ok", code="200", message="Success delete book").model_dump(
        exclude_none=True
    )
