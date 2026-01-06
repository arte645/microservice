from types import CoroutineType
from typing import Any, Optional
from authx import TokenPayload
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.ArticleRepository import ArticleRepository
from ..schemas.ArticleSchemas import CreateArticleSchema, ArticleResponseSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from ..models.ArticleModel import Article
from ..specifications.ArticleSpecifications import ArticleSpecification
from src.infrastructure.rabbitmq import publish_notification
from ..repositories.ApiKeysRepository import ApiKeysRepository
from ..specifications.ApiKeySpecifications import ApiKeySpecification


async def created_by_user(db: AsyncSession, article_id: str, user_id: str):
    results = await ArticleRepository(db).filter_by_spec(ArticleSpecification.created_by_user(user_id) &
                                       ArticleSpecification.article_id_is(article_id) & ArticleSpecification.not_deleted())
    return len(results)

async def status_is(db: AsyncSession, article_id: str, status):
    results = await ArticleRepository(db).filter_by_spec(ArticleSpecification.article_id_is(article_id)
                                                          & ArticleSpecification.not_deleted()
                                                          & ArticleSpecification.status_is(status))
    return len(results)


async def add_article(article: CreateArticleSchema, token_data: str, db: AsyncSession):
    article_id = uuid.uuid4()

    new_article = Article(
        article_id=article_id,
        title=article.title,
        description=article.description,
        body=article.body,
        taglist=article.taglist,
        user_id=token_data.sub
    )

    await ArticleRepository(db).add(new_article)
    
    return {"status": "created",
            "article_id": f"{article_id}"}


async def get_articles(db: AsyncSession, page: int, per_page: Optional[int]):
    articles = await ArticleRepository(db).filter_by_spec(page=page, per_page=per_page,
                                                          spec=ArticleSpecification.not_deleted())

    if not articles:
        raise HTTPException(status_code=404, detail="Not found")

    return {"data": [ArticleResponseSchema.model_validate(a).model_dump() for a in articles]}


async def get_article_by_article_id(db: AsyncSession, article_id: str):
    articles = await ArticleRepository(db).filter_by_spec(spec=ArticleSpecification.not_deleted() & ArticleSpecification.article_id_is(article_id=article_id))
    if not articles:
        raise HTTPException(status_code=404, detail="Not found")
    return {"data": ArticleResponseSchema.model_validate(articles[0]).model_dump()}


async def update_article_data(db: AsyncSession, article_id: str, updated_article: CreateArticleSchema, token_data: CoroutineType[Any, Any, TokenPayload]):
    user_id = token_data.sub

    if not await created_by_user(db, article_id, user_id):
        raise HTTPException(status_code=403, detail="Forbidden or non-existent")

    new_article = {
        "article_id": article_id,
        "title": updated_article.title,
        "description": updated_article.description,
        "body": updated_article.body,
        "taglist": updated_article.taglist
    }
    await ArticleRepository(db).update(new_article)
    return {"status": "updated"}


async def delete_article(db: AsyncSession, article_id: str, token_data: CoroutineType[Any, Any, TokenPayload]):
    user_id = token_data.sub

    if not await created_by_user(db, article_id, user_id):
        raise HTTPException(status_code=403, detail="Forbidden or non-existent")

    user = {
        "article_id": article_id,
        "is_deleted": True
    }
    await ArticleRepository(db).update(user)
    return {"status": "deleted"}

async def publish_article(db: AsyncSession, article_id: str, token_data: CoroutineType[Any, Any, TokenPayload]):
    user_id = token_data.sub

    if not await created_by_user(db, article_id, user_id):
        raise HTTPException(status_code=403, detail="Forbidden or non-existent")
    
    if not await status_is(db, article_id, status="DRAFT"):
        raise HTTPException(status_code=400, detail="Status isnt DRAFT")
    
    article = {
        "article_id": article_id,
        "status": "PENDING_PUBLISH"
    }
    await ArticleRepository(db).update(article)
    api_key = await ApiKeysRepository(db).filter_by_spec(ApiKeySpecification.api_is(description="backend"))
    if not api_key:
        raise HTTPException(status_code=500, detail="Api key for backend not found")
    await publish_notification({
        "event": "ARTICLE_MODERATE",
        "article_id": str(article_id),
        "author_id": user_id,
        "requested_by": api_key[0].key
    }, queue = "moderation")

    return {"status": "article is pending publish"}

async def reject_article(db: AsyncSession, article_id: str):  
    article = {
        "article_id": article_id,
        "status": "REJECTED"
    }
    await ArticleRepository(db).update(article)

    return {"status": "article is REJECTED"}

async def get_api_keys(db: AsyncSession):
    api_keys = await ApiKeysRepository(db).list()
    return {"data": [{ "key": api_key.key, "description": api_key.description} for api_key in api_keys]}