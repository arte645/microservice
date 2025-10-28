from fastapi import APIRouter, Depends
from src.schemas.UserSchemas import *
from src.models.Database import get_db
from src.controllers import UserController
from src.controllers.AuthorizationController import access_token_required

UserRouter = APIRouter()

@UserRouter.post("/users", tags=["users"])
def register_user(user: CreateUserSchema, db = Depends(get_db)):
    answer = UserController.register_user(user, db)
    return answer

@UserRouter.post("/users/auth", tags=["users"])
def authorize_user(user: LoginUserSchema, db = Depends(get_db)):
    answer = UserController.authorize_user(user, db)
    return answer

@UserRouter.get("/user", tags=["users"])
def get_users_info(token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = UserController.get_users_info(token_data, db)
    return answer

@UserRouter.put("/user/edit", tags=["users"])
def update_users_info(updated_user: CreateUserSchema, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = UserController.update_users_info(updated_user, user_token = token_data, db = db)
    return answer

@UserRouter.patch("/user/delete", tags=["users"])
def delete_user(token_data = Depends(access_token_required), db = Depends(get_db)):
    answer = UserController.delete_user(token_data, db)
    return answer