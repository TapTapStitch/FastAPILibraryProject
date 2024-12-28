from fastapi import FastAPI
from fastapi_pagination import add_pagination
from .routers import books

app = FastAPI(debug=True)
add_pagination(app)


@app.get("/")
async def healthcheck():
    return {"status": "healthy"}


app.include_router(books.router, prefix="/books", tags=["books"])
