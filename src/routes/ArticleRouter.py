from fastapi import APIRouter, Depends
from schemas.ArticleSchemas import *
from controllers.AuthorizationController import security

ArticleRouter = APIRouter()

ArticleRouter.post("/articles", tags=["articles"])
def add_article(article: CreateArticleSchema, token_data = Depends(security.access_token_required)):
    pass

ArticleRouter.get("/articles", tags=["articles"])
def get_articles():
    pass

ArticleRouter.get("/articles/{slug}", tags=["articles"])
def get_article():
    pass

ArticleRouter.put("/articles/{slug}", tags=["articles"])
def update_users_info(updated_article: CreateArticleSchema, token_data = Depends(security.access_token_required)):
    pass

ArticleRouter.patch("/articles/{slug}/delete", tags=["articles"])
def update_users_info(token_data = Depends(security.access_token_required)):
    pass
