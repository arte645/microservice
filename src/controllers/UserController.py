from src.repositories.UserRepository import UserRepository
from src.schemas.UserSchemas import CreateUserSchema
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from src.models.UserModel import User
from src.specifications.UserSpecifications import UserSpecification

def user_exist(user, db, user_id=None):
    return len(UserRepository(db).filter_by_spec((UserSpecification.existing_email(user.email) |
                                                UserSpecification.existing_username(user.username)) 
                                                & ~UserSpecification.is_deleted()
                                                & ~UserSpecification.id_is(user_id)))

def check_login_and_password(user, db):
    return UserRepository(db).filter_by_spec(UserSpecification.existing_password(user.password) &
                                                UserSpecification.existing_username(user.username) & ~UserSpecification.is_deleted())

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
        image_url = user.image_url,
        is_deleted = False
    )

    UserRepository(db).add(new_user)
    access_token = create_access_token(user_id)
    
    return {"access_token": access_token}

def authorize_user(user, db):
    user_data = check_login_and_password(user, db)
    if user_data:
        access_token = create_access_token(str(user_data[0].user_id))
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="Неправильно введён логин или пароль")
    

def get_users_info(user_token, db):
    return UserRepository(db).filter_by_spec(~UserSpecification.is_deleted() 
                                             & UserSpecification.id_is(user_token.sub))

def update_users_info(updated_user, user_token, db):
    user_id = user_token.sub
    
    if user_exist(updated_user, db, user_id):
        raise HTTPException(status_code=400, detail="Данный пользователь существует")
    
    new_user = {
        "user_id": user_id,
        "email": updated_user.email,
        "username": updated_user.username,
        "password": updated_user.password,
        "sex": updated_user.sex,
        "image_url": updated_user.image_url
    }
    UserRepository(db).update(new_user)
    return {"status":"ok"}

def delete_user(user_token, db):
    user_id = user_token.sub
    user = {
        "user_id": user_id,
        "is_deleted": True
    }
    UserRepository(db).update(user)
    return {"status":"ok"}
