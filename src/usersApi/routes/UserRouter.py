from fastapi import APIRouter, Depends
from ..schemas.UserSchemas import CreateUserSchema, LoginUserSchema, UserResponseSchema
from ..models.Database import get_db
from ..controllers import UserController
from ..controllers.AuthorizationController import access_token_required

UserRouter = APIRouter()

@UserRouter.post("/api/users/", tags=["users"])
async def register_user(user: CreateUserSchema, db = Depends(get_db)):
    answer = await UserController.register_user(user, db)
    return answer

@UserRouter.get("/api/users/", tags=["users"])
async def get_all_users(db = Depends(get_db)):
    answer = await UserController.get_all_users(db)
    return answer

@UserRouter.post("/api/users/auth/", tags=["users"])
async def authorize_user(user: LoginUserSchema, db = Depends(get_db)):
    answer = await UserController.authorize_user(user, db)
    return answer

@UserRouter.get("/api/users/me/", tags=["users"])
async def get_users_info(token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.get_users_info(token_data, db)
    return answer

@UserRouter.put("/api/users/me/", tags=["users"])
async def update_users_info(updated_user: CreateUserSchema, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.update_users_info(updated_user, user_token = token_data, db = db)
    return answer

@UserRouter.delete("/api/users/delete/", tags=["users"])
async def delete_user(token_data = Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.delete_user(token_data, db)
    return answer

@UserRouter.post("/api/users/subscribe/{target_user_id}", tags=["users"])
async def subscribe_to_user(target_user_id: str, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.subscribe_to_user(target_user_id, user_token = token_data, db = db)
    return answer

@UserRouter.post("/api/users/me/subscription-key/{subscription_key}", tags=["users"])
async def subscription_key(subscription_key: str, token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.subscription_key(subscription_key, user_token = token_data, db = db)
    return answer

@UserRouter.get("/api/users/me/subscriptions/", tags=["users"])
async def get_all_my_subscriptions(token_data=Depends(access_token_required), db = Depends(get_db)):
    answer = await UserController.get_all_my_subscriptions(user_token = token_data, db = db)
    return answer