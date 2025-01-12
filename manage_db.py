import argparse
from sqlalchemy_utils import database_exists, create_database, drop_database
import subprocess
from sqlalchemy import create_engine
from app.config import settings


def get_engine(use_test_db):
    db_url = settings.TEST_DATABASE_URL if use_test_db else settings.DATABASE_URL
    if not db_url:
        raise ValueError("Database URL not found in environment variables.")
    return create_engine(db_url)


def create_db(engine):
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{engine.url.database}' created successfully.")
    else:
        print(f"Database '{engine.url.database}' already exists.")


def drop_db(engine):
    if database_exists(engine.url):
        drop_database(engine.url)
        print(f"Database '{engine.url.database}' dropped successfully.")
    else:
        print(f"Database '{engine.url.database}' does not exist.")


def run_migrations(engine):
    create_db(engine)
    subprocess.run(["alembic", "upgrade", "head"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database management script.")
    parser.add_argument(
        "command",
        choices=["create", "drop", "migrate"],
        help="Command to execute: 'create' to create the database, 'drop' to drop the database, 'migrate' to run migrations.",
    )
    parser.add_argument(
        "--use-test-db",
        action="store_true",
        help="Use the test database specified in the environment variables.",
    )
    args = parser.parse_args()

    engine = get_engine(args.use_test_db)

    if args.command == "create":
        create_db(engine)
    elif args.command == "drop":
        drop_db(engine)
    elif args.command == "migrate":
        run_migrations(engine)
