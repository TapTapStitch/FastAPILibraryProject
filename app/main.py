from fastapi import FastAPI
from .config import Base, engine
from .routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def healthcheck():
    return {"status": "healthy"}


app.include_router(books.router, prefix="/books", tags=["books"])
