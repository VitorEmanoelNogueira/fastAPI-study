from fastapi import FastAPI, Query
from typing import Annotated
from models import Book
from crud import create_book, get_book, get_all_books, update_book, delete_book
from uuid import UUID

error_message = {"error": "Book not found"}
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, welcome to the book catalog API!"}

@app.post("/books/")
def add_book(book: Book):
    return create_book(book)

@app.get("/books/{book_id}")
def read_book(book_id: UUID):
    book = get_book(book_id)
    if book:
        return book
    return error_message

@app.get("/books/")
def read_all_books(
    author: Annotated[ str | None, Query(min_length = 1)] = None,
    year: Annotated[int  | None, Query(ge=0, le=2100)] = None
):
    books = get_all_books(author, year)
    if books:
        return books
    return error_message

@app.put("/books/{book_id}")
def modify_book(book_id: UUID, book: Book):
    updated_book = update_book(book_id, book)
    if updated_book:
        return updated_book
    return error_message

@app.delete("/books/{book_id}")
def remove_book(book_id: UUID):
    deleted_book = delete_book(book_id)
    if deleted_book:
        return {"message": f"Book of id {book_id} deleted successfully"}
    return error_message