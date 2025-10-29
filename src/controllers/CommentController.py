from src.repositories.CommentRepository import CommentRepository
from src.repositories.ArticleRepository import ArticleRepository 
from src.schemas.CommentSchemas import CreateCommentSchema, CommentResponseSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from src.models.CommentModel import Comment
from src.specifications.CommentSpecifications import CommentSpecification

def article_is_deleted(slug, db):
    return ArticleRepository(db).get_by_id(slug).is_deleted

def user_is_author(user_id, comment_id, db):
    return len(CommentRepository(db).filter_by_spec(CommentSpecification.user_is_author(user_id) 
                                                    & CommentSpecification.comment_id_is(comment_id)))

def add_comment(comment: CreateCommentSchema, slug: str, token_data, db):
    if article_is_deleted(slug, db):
        raise HTTPException(status_code = 404, detail="Article not found")
    
    comment_id = str(uuid.uuid4())
    new_comment = Comment(
        comment_id = comment_id,
        body = comment.body,
        article_id = slug,
        user_id =token_data.sub
    )

    CommentRepository(db).add(new_comment)
    return {"status": "created",
            "comment_id": f"{comment_id}"}

def get_comments(slug: str, db):
    if article_is_deleted(slug, db):
        raise HTTPException(status_code = 404, detail="Article not found")
    
    comments = CommentRepository(db).filter_by_spec(~CommentSpecification.comment_is_deleted())
    return [CommentResponseSchema.model_validate(c).model_dump() for c in comments]

def delete_comment(slug: str, id: str, token_data, db):
    if article_is_deleted(slug, db) or not user_is_author(token_data.sub, id, db):
        raise HTTPException(status_code = 404, detail="Article not found")

    comment = {
        "comment_id": id,
        "is_deleted": True
    }

    CommentRepository(db).update(comment)
    return {"status": "deleted"}
