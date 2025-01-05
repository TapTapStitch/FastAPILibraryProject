from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import books, authors

app = FastAPI(debug=True)

app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])


@app.get("/health")
async def healthcheck():
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")
