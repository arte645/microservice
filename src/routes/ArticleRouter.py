from fastapi import APIRouter, Depends
from src.schemas.ArticleSchemas import *
from src.controllers.AuthorizationController import security
from src.models.Database import get_db

ArticleRouter = APIRouter()

@ArticleRouter.post("/articles", tags=["articles"])
def add_article(article: CreateArticleSchema, token_data = Depends(security.access_token_required), db = Depends(get_db)):
    pass

@ArticleRouter.get("/articles", tags=["articles"])
def get_articles(db = Depends(get_db)):
    pass

@ArticleRouter.get("/articles/{slug}", tags=["articles"])
def get_article(db = Depends(get_db)):
    pass

@ArticleRouter.put("/articles/{slug}", tags=["articles"])
def update_users_info(updated_article: CreateArticleSchema, token_data = Depends(security.access_token_required), db = Depends(get_db)):
    pass

@ArticleRouter.patch("/articles/{slug}/delete", tags=["articles"])
def update_users_info(token_data = Depends(security.access_token_required), db = Depends(get_db)):
    pass
