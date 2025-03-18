from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre

book_sort_fields = {
    "title": Book.title,
    "description": Book.description,
    "year_of_publication": Book.year_of_publication,
    "isbn": Book.isbn,
    "series": Book.series,
    "file_link": Book.file_link,
    "edition": Book.edition,
    "created_at": Book.created_at,
    "updated_at": Book.updated_at,
}

author_sort_fields = {
    "name": Author.name,
    "surname": Author.surname,
    "year_of_birth": Author.year_of_birth,
    "biography": Author.biography,
    "created_at": Author.created_at,
    "updated_at": Author.updated_at,
}

genre_sort_fields = {
    "name": Genre.name,
    "description": Genre.description,
    "created_at": Genre.created_at,
    "updated_at": Genre.updated_at,
}
