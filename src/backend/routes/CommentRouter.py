from fastapi import APIRouter, Depends
from ..schemas.CommentSchemas import CreateCommentSchema, CommentResponseSchema
from ..controllers.AuthorizationController import access_token_required
from ..models.Database import get_db
from ..controllers import CommentController
from typing import List

CommentRouter = APIRouter()

@CommentRouter.post("/articles/{article_id}/comments/", tags=["comments"])
async def add_comment(article_id: str, comment: CreateCommentSchema,
                      token_data = Depends(access_token_required),
                      db = Depends(get_db)):
    answer = await CommentController.add_comment(comment, article_id, token_data, db)
    return answer


@CommentRouter.get("/articles/{article_id}/comments/", tags=["comments"])
async def get_comments(article_id: str, db = Depends(get_db)):
    answer = await CommentController.get_comments(article_id, db)
    return answer


@CommentRouter.delete("/articles/{article_id}/comments/{id}/", tags=["comments"])
async def delete_comment(article_id: str, id: str, token_data = Depends(access_token_required), db = Depends(get_db)):
    answer = await CommentController.delete_comment(article_id, id, token_data, db)
    return answer
