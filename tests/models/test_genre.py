from sqlalchemy import select
from app.models.genre import Genre


def test_create_genre(session):
    new_genre = Genre(
        name="Science Fiction",
        description="A genre that explores imaginative and futuristic concepts.",
    )
    session.add(new_genre)
    session.commit()
    stmt = select(Genre).where(Genre.name == "Science Fiction")
    result = session.execute(stmt).scalar_one_or_none()
    assert result is not None
    assert result.name == "Science Fiction"
    assert (
        result.description
        == "A genre that explores imaginative and futuristic concepts."
    )
