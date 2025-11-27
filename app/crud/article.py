from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas

router = APIRouter()

# Create Article
@router.post("/articles", response_model=schemas.ArticleOut)
def create_article(payload: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = models.Article(
        title=payload.title,
        content=payload.content,
        author_name=payload.author_name
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

# list All Articles
@router.get("/articles", response_model=list[schemas.ArticleOut])
def list_articles(db: Session = Depends(get_db)):
    return db.query(models.Article).all()

# Read Single Article
@router.get("/articles/{article_id}", response_model=schemas.ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")
    return article

# Update Article
@router.put("/articles/{article_id}", response_model=schemas.ArticleOut)
def update_article(article_id: int, payload: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = db.query(models.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")

    article.title = payload.title
    article.content = payload.content
    article.author_name = payload.author_name

    db.commit()
    db.refresh(article)
    return article
# Delete Article
@router.delete("/articles/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(models.Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="article not found")

    db.delete(article)
    db.commit()
    return {"msg": "deleted"}