from fastapi import APIRouter, Depends
from schemas.UserSchemas import *
from controllers.AuthorizationController import security

UserRouter = APIRouter()

UserRouter.post("/users", tags=["users"])
def register_user(user: CreateUserSchema):
    pass

UserRouter.get("/users/auth", tags=["users"])
def authorize_user(user: CreateUserSchema):
    pass

UserRouter.get("/user", tags=["users"])
def get_users_info(token_data = Depends(security.access_token_required)):
    pass

UserRouter.put("/user/edit", tags=["users"])
def update_users_info(updated_user: CreateUserSchema, token_data = Depends(security.access_token_required)):
    pass

UserRouter.patch("/user/delete", tags=["users"])
def update_users_info(token_data = Depends(security.access_token_required)):
    pass