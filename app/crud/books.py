# app/crud/books.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter()

# Create Book (assign to current user)
@router.post("/books", response_model=schemas.BookOut)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    book = models.Book(
        title=payload.title,
        content=payload.content,
        author_name=payload.author_name,
        user_id=current_user.id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

# list user's books
@router.get("/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Book).filter(models.Book.user_id == current_user.id).all()

# Read Single Book
@router.get("/books/{book_id}", response_model=schemas.BookOut)
def get_books(book_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).get(book_id)
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")
    return book

# Update Book
@router.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(book_id: int, payload: schemas.BookCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).get(book_id)
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

    book.title = payload.title
    book.content = payload.content
    book.author_name = payload.author_name

    db.commit()
    db.refresh(book)
    return book

# Delete Book
@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    book = db.query(models.Book).get(book_id)
    if not book or book.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="book not found")

    db.delete(book)
    db.commit()
    return {"msg": "deleted"}
