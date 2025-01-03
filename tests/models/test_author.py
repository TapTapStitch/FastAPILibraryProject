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
