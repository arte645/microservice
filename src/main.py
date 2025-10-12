from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from src.models.Database import SessionLocal
from src.routes import *
import src.models as models

app = FastAPI()

app.include_router(UserRouter)
app.include_router(ArticleRouter)
app.include_router(CommentRouter)

# Dependency: получение сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).all()
    return articles