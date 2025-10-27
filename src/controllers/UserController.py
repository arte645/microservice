from src.repositories.UserRepository import UserRepository
from src.schemas.UserSchemas import CreateUserSchema
from .AuthorizationController import create_access_token
from fastapi import HTTPException
import uuid
from src.models.UserModel import User
from src.specifications.UserSpecifications import UserSpecification

def user_exist(user, db):
    return len(UserRepository(db).filter_by_spec(UserSpecification.existing_email(user.email) |
                                                UserSpecification.existing_username(user.username)))

def register_user(user: CreateUserSchema, db):
    if user_exist(user, db):
        raise HTTPException(status_code=400, detail="Данный пользователь существует")
    user_id = str(uuid.uuid4())

    new_user = User(
        user_id = user_id,
        email = user.email,
        username = user.username,
        password = user.password,
        sex = user.sex,
        image_url = user.image_url
    )

    UserRepository(db).add(new_user)
    access_token = create_access_token(user_id)
    
    return {"access_token": access_token}

def authorize_user(user, db):
    pass

def get_users_info(user_id, db):
    pass

def update_users_info(updated_user, user_id, db):
    pass

def delete_user(user_id, db):
    pass