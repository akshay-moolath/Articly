# app/crud/user.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas

router = APIRouter()

@router.post("/users", response_model=schemas.UserOut)
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.username == payload.username).first():#check for username exists
        raise HTTPException(status_code=400, detail="username already exists")
    if db.query(models.User).filter(models.User.email == payload.email).first():#check for email exists
        raise HTTPException(status_code=400, detail="email already exists")

    user = models.User(
        username=payload.username,
        email=payload.email,
        password=payload.password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@router.post("/login")
def login_user(payload: schemas.LoginSchema, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if user.password != payload.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return {"success": True, "username": user.username}

