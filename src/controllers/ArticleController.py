from src.repositories.ArticleRepository import ArticleRepository
from src.schemas.ArticleSchemas import CreateArticleSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from src.models.ArticleModel import Article
from src.specifications.ArticleSpecifications import ArticleSpecification

def created_by_user(db, slug, user_id):
    return len(ArticleRepository(db).filter_by_spec(ArticleSpecification.created_by_user(user_id)&
                                                    ArticleSpecification.slug_is(slug)&ArticleSpecification.not_deleted()))


def add_article(article: CreateArticleSchema, token_data: str, db):
    article_id = str(uuid.uuid4())

    new_article = Article(
        article_id = article_id,
        title = article.title,
        description = article.description,
        body = article.body,
        taglist = article.taglist,
        user_id= token_data.sub
    )

    ArticleRepository(db).add(new_article)

    return {"status": "created"}

def get_articles(db, page, per_page):
    articles = ArticleRepository(db).filter_by_spec(page=page, per_page=per_page, spec=ArticleSpecification.not_deleted())

    if not articles:
        raise HTTPException(status_code=404, detail="Not found")

    return articles

def get_article_by_slug(db, slug):
    article = ArticleRepository(db).filter_by_spec(spec=ArticleSpecification.not_deleted() & ArticleSpecification.slug_is(slug=slug))
    if not article:
        raise HTTPException(status_code=404, detail="Not found")
    return article

def update_article_data(db, slug, updated_article, token_data):
    user_id = token_data.sub
    
    if not created_by_user(db, slug, user_id):
        raise HTTPException(status_code=403, detail="Forbidden or non-existent")
    
    new_article = {
        "article_id": slug,
        "title": updated_article.title,
        "description": updated_article.description,
        "body": updated_article.body,
        "taglist": updated_article.taglist
    }
    ArticleRepository(db).update(new_article)
    return {"status": "updated"}

def delete_article(db, slug, token_data):
    user_id = token_data.sub

    if not created_by_user(db, slug, user_id):
        raise HTTPException(status_code=403, detail="Forbidden or non-existent")
    
    user = {
        "article_id": slug,
        "is_deleted": True
    }
    ArticleRepository(db).update(user)
    return {"status": "deleted"}