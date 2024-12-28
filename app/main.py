from fastapi import FastAPI
from .routers import books

app = FastAPI()


@app.get("/")
async def healthcheck():
    return {"status": "healthy"}


app.include_router(books.router, prefix="/books", tags=["books"])
