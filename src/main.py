from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from src.models.Database import SessionLocal, get_db
from src.routes import *
import src.models as models

app = FastAPI()

@app.get("/health", tags=["health"],
         summary="Проверить состояние сервиса", description="Возвращает статус работы сервиса.")
def health():
    return {"status": "ok"}


@app.get("/articles")
def get_articles(db: Session = Depends(get_db)):
    articles = db.query(models.Article).offset(2).limit(1).all()
    return articles


app.include_router(UserRouter)
app.include_router(ArticleRouter)
app.include_router(CommentRouter)