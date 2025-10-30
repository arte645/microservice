from src.repositories.CommentRepository import CommentRepository
from src.repositories.ArticleRepository import ArticleRepository
from src.schemas.CommentSchemas import CreateCommentSchema, CommentResponseSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from src.models.CommentModel import Comment
from src.specifications.CommentSpecifications import CommentSpecification


async def article_is_deleted(slug, db):
    article = await ArticleRepository(db).get_by_id(slug)
    return article is None or article.is_deleted


async def user_is_author(user_id, comment_id, db):
    results = await CommentRepository(db).filter_by_spec(CommentSpecification.user_is_author(user_id)
                                                       & CommentSpecification.comment_id_is(comment_id))
    return len(results)


async def add_comment(comment: CreateCommentSchema, slug: str, token_data, db):
    if await article_is_deleted(slug, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comment_id = uuid.uuid4()
    new_comment = Comment(
        comment_id=comment_id,
        body=comment.body,
        article_id=slug,
        user_id=token_data.sub
    )

    await CommentRepository(db).add(new_comment)
    return {"status": "created",
            "comment_id": f"{comment_id}"}


async def get_comments(slug: str, db):
    if await article_is_deleted(slug, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comments = await CommentRepository(db).filter_by_spec(~CommentSpecification.comment_is_deleted() & CommentSpecification.article_is(slug))
    return [CommentResponseSchema.model_validate(c).model_dump() for c in comments]


async def delete_comment(slug: str, id: str, token_data, db):
    if await article_is_deleted(slug, db) or not await user_is_author(token_data.sub, id, db):
        raise HTTPException(status_code=404, detail="Article not found")

    comment = {
        "comment_id": id,
        "is_deleted": True
    }

    await CommentRepository(db).update(comment)
    return {"status": "deleted"}
