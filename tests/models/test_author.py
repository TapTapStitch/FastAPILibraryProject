from app.models.author import Author


def test_create_author(session):
    new_author = Author(
        name="John",
        surname="Doe",
        year_of_birth=1980,
        biography="An accomplished author.",
    )
    session.add(new_author)
    session.commit()

    retrieved_author = (
        session.query(Author).filter_by(name="John", surname="Doe").first()
    )
    assert retrieved_author is not None
    assert retrieved_author.name == "John"
    assert retrieved_author.surname == "Doe"
    assert retrieved_author.year_of_birth == 1980
    assert retrieved_author.biography == "An accomplished author."


def test_author_books_relationship(session):
    from app.models.book import Book

    new_author = Author(name="Jane", surname="Smith")
    new_book = Book(title="Sample Book")
    new_author.books.append(new_book)
    session.add(new_author)
    session.commit()

    retrieved_author = (
        session.query(Author).filter_by(name="Jane", surname="Smith").first()
    )
    assert retrieved_author is not None
    assert len(retrieved_author.books) == 1
    assert retrieved_author.books[0].title == "Sample Book"
