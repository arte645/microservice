from fastapi import APIRouter, Depends
from src.schemas.CommentSchemas import *
from src.controllers.AuthorizationController import access_token_required
from src.models.Database import get_db
from src.controllers import CommentController
from typing import List

CommentRouter = APIRouter()

@CommentRouter.post("/articles/{slug}/comments", tags=["comments"])
def add_comment(slug:str, comment: CreateCommentSchema, 
                token_data = Depends(access_token_required),  
                db = Depends(get_db)):
    answer = CommentController.add_comment(comment, slug, token_data, db)
    return answer

@CommentRouter.get("/articles/{slug}/comments", tags=["comments"], response_model=List[CommentResponseSchema])
def get_comments(slug: str, db = Depends(get_db)):
    answer = CommentController.get_comments(slug, db)
    return answer

@CommentRouter.patch("/articles/{slug}/comments/{id}/delete", tags=["comments"])
def delete_comment(slug: str, id: str, token_data = Depends(access_token_required), db = Depends(get_db)):
    answer = CommentController.delete_comment(slug, id, token_data, db)
    return answer
