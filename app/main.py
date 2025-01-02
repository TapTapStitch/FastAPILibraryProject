from fastapi import FastAPI
from .routers import books, authors

app = FastAPI(debug=True)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])


@app.get("/")
async def healthcheck():
    return {"status": "healthy"}
