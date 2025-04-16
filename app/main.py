from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers.api.v1 import authors, genres, sessions, books
from app.admin.index import admin

app = FastAPI(debug=True)
admin.mount_to(app)

app.include_router(books.router, prefix="/api/v1/books", tags=["v1 books"])
app.include_router(authors.router, prefix="/api/v1/authors", tags=["v1 authors"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["v1 genres"])
app.include_router(sessions.router, prefix="/api/v1/sessions", tags=["v1 sessions"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
