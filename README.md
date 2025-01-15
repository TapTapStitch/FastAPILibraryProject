# FastApiLibraryProject

FastApiLibraryProject is a web application designed to manage a library system efficiently. Built with FastAPI, it offers high performance and easy-to-use features for handling books, authors, and user interactions.

## Features

- **Book Management:** Add, update, delete, and search for books.
- **Author Management:** Manage author information and their associated works.
- **User Authentication:** Secure user login and registration system.
- **Search Functionality:** Advanced search options for books and authors.

## Installation

1. Ensure you have Python 3.13 or higher and PostgreSQL installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/TapTapStitch/FastAPILibraryProject.git
   ```
3. Navigate to the project directory:
   ```bash
   cd MyFastApiLibraryProject
   ```
4. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source env/bin/activate  # On Windows: `env\Scripts\activate`
   ```
5. Install the dependencies:
   ```bash
   pip install poetry
   poetry install # For Production: `poetry install --without dev`
   ```

## Usage

To run the project, use the following command:
   ```bash
   fastapi dev   # For Production: `fastapi run`
   ```

## Configuration

To configure project, follow these steps:

1. Copy the Example Environment File:
   ```bash
   cp .env.example .env   # On Windows: `copy .env.example .env`
   ```

2. Edit the .env File:
   ```markdown
   Ensure that all necessary environment variables are correctly set to match your development or production environment requirements.
   ```

## Testing

To run tests use:
   ```bash
   pytest
   ```
Tests will be executed in random order, coverage report will be saved to project root.

## DB Management

To create migrate or drop database use following command:
   ```bash
   python manage_db.py create | migrate | drop  # To work with testing db use such flag: `--use-test-db`, testing db is not using migrations so use create | drop
   ```

To seed database with random data use following command:
   ```bash
   python -m migrations.seeds
   ```

