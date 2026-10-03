from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
books = {}
next_id = 1


class Book(BaseModel):
    title: str
    author: str
    price: float


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    price: Optional[float] = None


@app.get('/books')
def get_all_books():
    return books


@app.post('/books', status_code=201)
def create_book(book: Book):
    global next_id
    book_id = next_id
    books[book_id] = book.model_dump()
    next_id += 1
    return {'id': book_id, **books[book_id]}


@app.put('/books/{book_id}')
def update_book(book_id: int, update: BookUpdate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail='Not found')
    books[book_id].update(
        update.model_dump(exclude_unset=True, exclude_none=True)
    )
    return books[book_id]


@app.delete('/books/{book_id}')
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail='Not found')
    del books[book_id]
    return {'message': 'Book deleted successfully'}
