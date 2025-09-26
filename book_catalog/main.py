from fastapi import FastAPI, Query, status, HTTPException
from typing import Annotated
from models import Book
from storage import books
from crud import create_book, get_book, get_all_books, update_book, delete_book
from uuid import UUID

app = FastAPI()
error_message = "Book not found"

@app.get("/")
async def root():
    return {
        "message": "Hello, welcome to the book catalog API! Read the documentation for more info.",
        "status": "ok",
        "total_books": len(books),
        "links": {
            "all_books": "/books/",
            "create_book": "/books/"
            }
        }

@app.post("/books/", status_code=status.HTTP_201_CREATED)
def add_book(book: Book):
    return create_book(book)

@app.get("/books/{book_id}")
def read_book(book_id: UUID):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail=error_message)
    return book

@app.get("/books/")
def read_all_books(
    author: Annotated[ str | None, Query(min_length = 1)] = None,
    year: Annotated[int  | None, Query(ge=0, le=2100)] = None
):
    return get_all_books(author, year)

@app.put("/books/{book_id}", status_code=status.HTTP_200_OK)
def modify_book(book_id: UUID, book: Book):
    updated_book = update_book(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail=error_message)
    return updated_book

@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
def remove_book(book_id: UUID):
    deleted_book = delete_book(book_id)
    if not deleted_book:
        raise HTTPException(status_code=404, detail=error_message)
    return {"message": f"Book of id {book_id} deleted successfully"}