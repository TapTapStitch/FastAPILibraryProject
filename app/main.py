from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .routers import books, authors

app = FastAPI(debug=True)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])


@app.get("/")
async def healthcheck():
    return {"status": "healthy"}


add_pagination(app)
