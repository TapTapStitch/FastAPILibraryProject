from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.models import *  # Preload models and their dependencies
from app.routers import books, authors, genres, sessions

app = FastAPI(debug=True)

app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(authors.router, prefix="/api/v1/authors", tags=["authors"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["sessions"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
