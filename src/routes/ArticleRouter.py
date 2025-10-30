from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from src.schemas.ArticleSchemas import CreateArticleSchema, ArticleResponseSchema
from src.controllers.AuthorizationController import access_token_required
from src.models.Database import get_db
from src.controllers import ArticleController

ArticleRouter = APIRouter()

@ArticleRouter.post("/articles", tags=["articles"])
async def add_article(article: CreateArticleSchema, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.add_article(article, token_data, db)
    return answer

@ArticleRouter.get("/articles", tags=["articles"], response_model=List[ArticleResponseSchema])
async def get_articles(db = Depends(get_db), page: int = Query(0, ge=0),
                 per_page: Optional[int] = Query(None, ge=0, le=100)):
    answer = await ArticleController.get_articles(db, page, per_page)
    return answer

@ArticleRouter.get("/articles/{slug}", tags=["articles"], response_model=ArticleResponseSchema)
async def get_article_by_slug(slug: str, db = Depends(get_db)):
    answer = await ArticleController.get_article_by_slug(db, slug)
    return answer

@ArticleRouter.put("/articles/{slug}", tags=["articles"])
async def update_article_data(updated_article: CreateArticleSchema, slug: str , token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.update_article_data(db, slug, updated_article, token_data)
    return answer

@ArticleRouter.patch("/articles/{slug}/delete", tags=["articles"])
async def delete_article(slug: str, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await ArticleController.delete_article(db, slug, token_data)
    return answer
