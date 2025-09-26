# 📚 Book Catalog API

An API to manage a book catalog with basic functionalities using **FastAPI**.

Run the app and access the interactive API docs at http://localhost:8000/docs or /redoc.

---

## Requirements

### 1. Books CRUD
- **POST** `/books/` → create a book  
- **GET** `/books/` → list all books  
- **GET** `/books/{book_id}` → get a specific book  
- **PUT** `/books/{book_id}` → update book data  
- **DELETE** `/books/{book_id}` → remove a book  

### 2. Book Pydantic Model
- `id` (UUID, auto-generated)
- `title` (str, required, max 100 chars)
- `author` (str, required)
- `year` (int, optional, between 0 and 2100)
- `price` (float, optional)
  

### 3. Extra Validations
- Title can’t be empty  
- Year must be in the allowed range  
- Price (if present) must be positive  

### 4. Filtered Listing
- **GET** `/books/?author=Author` → return only books from this author  
- **GET** `/books/?year=2020` → return only books from this year  

### 5. Custom Return Messages
- If a book is not found → return `404` with JSON message  
- On delete → return JSON confirming the removal  

---

## Next Steps
- [x] Implement the Book model with Pydantic  
- [x] Create CRUD endpoints  
- [x] Add filters for author and year  
- [x] Customize error and delete responses  

---

## Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/)  
- [Pydantic](https://docs.pydantic.dev/)  

