from fastapi import APIRouter, Depends
from schemas.CommentSchemas import *
from controllers.AuthorizationController import security

CommentRouter = APIRouter()

CommentRouter.post("/articles/{slug}/comments", tags=["comments"])
def add_comment(comment: CreateCommentSchema, token_data = Depends(security.access_token_required)):
    pass

CommentRouter.get("/articles/{slug}/comments", tags=["comments"])
def get_comments():
    pass

CommentRouter.patch("articles/{slug}/comments/{id}/delete", tags=["comments"])
def delete_comment(token_data = Depends(security.access_token_required)):
    pass
