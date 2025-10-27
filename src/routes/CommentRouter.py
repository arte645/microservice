from fastapi import APIRouter, Depends
from src.schemas.CommentSchemas import *
from src.controllers.AuthorizationController import security
from src.models.Database import get_db

CommentRouter = APIRouter()

@CommentRouter.post("/articles/{slug}/comments", tags=["comments"])
def add_comment(comment: CreateCommentSchema, token_data = Depends(security.access_token_required),  db = Depends(get_db)):
    pass

@CommentRouter.get("/articles/{slug}/comments", tags=["comments"])
def get_comments(db = Depends(get_db)):
    pass

@CommentRouter.patch("articles/{slug}/comments/{id}/delete", tags=["comments"])
def delete_comment(token_data = Depends(security.access_token_required), db = Depends(get_db)):
    pass
