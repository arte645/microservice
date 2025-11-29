from types import CoroutineType
from typing import Any
from authx import TokenPayload
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.CommentRepository import CommentRepository
from ..repositories.ArticleRepository import ArticleRepository
from ..schemas.CommentSchemas import CreateCommentSchema, CommentResponseSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from ..models.CommentModel import Comment
from ..specifications.CommentSpecifications import CommentSpecification


async def article_is_deleted(article_id: str, db: AsyncSession):
    article = await ArticleRepository(db).get_by_id(article_id)
    return article is None or article.is_deleted


async def user_is_author(user_id: str, comment_id: str, db: AsyncSession):
    results = await CommentRepository(db).filter_by_spec(CommentSpecification.user_is_author(user_id)
                                                       & CommentSpecification.comment_id_is(comment_id))
    return len(results)


async def add_comment(comment: CreateCommentSchema, article_id: str, token_data: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    if await article_is_deleted(article_id, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comment_id = uuid.uuid4()
    new_comment = Comment(
        comment_id=comment_id,
        body=comment.body,
        article_id=article_id,
        user_id=token_data.sub
    )

    await CommentRepository(db).add(new_comment)
    return {"status": "created",
            "comment_id": f"{comment_id}"}


async def get_comments(article_id: str, db: AsyncSession):
    if await article_is_deleted(article_id, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comments = await CommentRepository(db).filter_by_spec(~CommentSpecification.comment_is_deleted() & CommentSpecification.article_is(article_id))
    return {"data": [CommentResponseSchema.model_validate(c).model_dump() for c in comments]}


async def delete_comment(article_id: str, id: str, token_data: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    if await article_is_deleted(article_id, db) or not await user_is_author(token_data.sub, id, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comment = {
        "comment_id": id,
        "is_deleted": True
    }

    await CommentRepository(db).update(comment)
    return {"status": "deleted"}
