from models import Book
from storage import books
from uuid import uuid4

# CREATE
def create_book(book: Book):
    book_id = uuid4()
    books[book_id] = book.model_dump()
    return {"id": book_id, **books[book_id]}

# READ
def get_book(book_id):
    book = books.get(book_id)
    if book:
        return {"id": book_id, **book}
    return None

def get_all_books():
    return [{"id": book_id, **book} for book_id, book in books.items()]
    
    
# UPDATE
def update_book(book_id, book: Book):
    if book_id in books:
        books[book_id] = book.model_dump()
        return {"id": book_id, **books[book_id]}
    return None
    
#DELETE
def delete_book(book_id):
        return books.pop(book_id, None)
    
    