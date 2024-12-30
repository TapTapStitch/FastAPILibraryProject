import argparse
from sqlalchemy_utils import database_exists, create_database, drop_database
import subprocess
from app.config import engine

def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{engine.url.database}' created successfully.")
    else:
        print(f"Database '{engine.url.database}' already exists.")

def drop_db():
    if database_exists(engine.url):
        drop_database(engine.url)
        print(f"Database '{engine.url.database}' dropped successfully.")
    else:
        print(f"Database '{engine.url.database}' does not exist.")

def run_migrations():
    create_db()
    subprocess.run(["alembic", "upgrade", "head"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database management script.")
    parser.add_argument("command", choices=["create", "drop", "migrate"],
                        help="Command to execute: 'create' to create the database, 'drop' to drop the database, 'migrate' to run migrations.")
    args = parser.parse_args()

    if args.command == "create":
        create_db()
    elif args.command == "drop":
        drop_db()
    elif args.command == "migrate":
        run_migrations()
