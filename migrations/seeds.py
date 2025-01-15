import random
from faker import Faker
from sqlalchemy.orm import Session
from app.models import Author, Book, Genre, User
from app.config import SessionLocal
from passlib.context import CryptContext

fake = Faker()

hashed_password = CryptContext(schemes=["bcrypt"], deprecated="auto").hash("password")


def create_authors(session: Session, count: int = 300):
    authors = []
    for _ in range(count):
        author = Author(
            name=fake.first_name(),
            surname=fake.last_name(),
            year_of_birth=fake.year(),
            biography=fake.text(),
        )
        session.add(author)
        authors.append(author)
    session.commit()
    return authors


def create_books(session: Session, authors: list, genres: list, count: int = 300):
    for _ in range(count):
        book = Book(
            title=fake.sentence(nb_words=4),
            description=fake.text(),
            year_of_publication=fake.year(),
            isbn=fake.isbn13(),
        )
        # Assign random authors and genres
        book.authors = random.sample(authors, k=random.randint(1, 3))
        book.genres = random.sample(genres, k=random.randint(1, 2))
        session.add(book)
    session.commit()


def create_genres(session: Session, count: int = 300):
    genres = []
    for _ in range(count):
        genre = Genre(
            name=fake.word(),
            description=fake.text(),
        )
        session.add(genre)
        genres.append(genre)
    session.commit()
    return genres


def create_users(session: Session, count: int = 300):
    for _ in range(count):
        user = User(
            email=fake.email(),
            hashed_password=hashed_password,
            name=fake.first_name(),
            surname=fake.last_name(),
        )
        session.add(user)
    session.commit()


session = SessionLocal()
authors = create_authors(session)
genres = create_genres(session)
create_books(session, authors, genres)
create_users(session)
session.close()
