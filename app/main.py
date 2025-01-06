from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .models import *  # Preload models and their dependencies
from .routers import books, authors, genres

app = FastAPI(debug=True)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
