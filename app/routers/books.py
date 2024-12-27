from fastapi import APIRouter
from fastapi import Depends
from ..config import get_db
from sqlalchemy.orm import Session
from ..schemas.book import BookSchema, ChangeBookSchema
from ..crud import book as crud

router = APIRouter()


@router.get("/", response_model=list[BookSchema])
async def get_books(db: Session = Depends(get_db)):
    books = crud.get_books(db)
    return books


@router.get(
    "/{book_id}",
    response_model=BookSchema,
    responses={404: {"detail": "Book not found"}},
)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id=book_id)
    return book


@router.post("/", response_model=BookSchema, status_code=201)
async def create_book_service(book: ChangeBookSchema, db: Session = Depends(get_db)):
    book = crud.create_book(db, title=book.title, description=book.description)
    return book


@router.patch(
    "/{book_id}",
    response_model=BookSchema,
    responses={404: {"detail": "Book not found"}},
)
async def update_book(
    book_id: int, book: ChangeBookSchema, db: Session = Depends(get_db)
):
    book = crud.update_book(
        db,
        book_id=book_id,
        title=book.title,
        description=book.description,
    )
    return book


@router.delete(
    "/{book_id}", status_code=204, responses={404: {"detail": "Book not found"}}
)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    crud.remove_book(db, book_id=book_id)
    return None
