from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from ..schemas.ArticleSchemas import CreateArticleSchema, ArticleResponseSchema
from ..controllers.AuthorizationController import access_token_required, inner_token_required
from ..models.Database import get_db
from ..controllers import ArticleController

ArticleRouter = APIRouter()

@ArticleRouter.post("/articles/", tags=["articles"])
async def add_article(article: CreateArticleSchema, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.add_article(article, token_data, db)
    return answer

@ArticleRouter.get("/articles/", tags=["articles"])
async def get_articles(db = Depends(get_db), page: int = Query(0, ge=0),
                 per_page: Optional[int] = Query(None, ge=0, le=100)):
    answer = await ArticleController.get_articles(db, page, per_page)
    return answer

@ArticleRouter.get("/articles/{article_id}/", tags=["articles"])
async def get_article_by_article_id(article_id: str, db = Depends(get_db)):
    answer = await ArticleController.get_article_by_article_id(db, article_id)
    return answer

@ArticleRouter.put("/articles/{article_id}/", tags=["articles"])
async def update_article_data(updated_article: CreateArticleSchema, article_id: str , token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.update_article_data(db, article_id, updated_article, token_data)
    return answer

@ArticleRouter.delete("/articles/{article_id}/", tags=["articles"])
async def delete_article(article_id: str, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.delete_article(db, article_id, token_data)
    return answer

@ArticleRouter.post("/articles/{article_id}/publish", tags=["articles"])
async def publish_article(article_id: str, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.publish_article(db, article_id, token_data)
    return answer

@ArticleRouter.put("/articles/{article_id}/reject", tags=["articles"])
async def reject_article(article_id: str, token_data=Depends(inner_token_required), db = Depends(get_db)):
    answer = await ArticleController.reject_article(db, article_id)
    return answer

@ArticleRouter.get("/articles/get_api_keys", tags=["articles"])
async def get_api_keys(db = Depends(get_db)):
    answer = await ArticleController.get_api_keys(db)
    return answer