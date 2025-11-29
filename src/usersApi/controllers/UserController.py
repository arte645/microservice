from types import CoroutineType
from typing import Any
from authx import TokenPayload
from ..repositories.UserRepository import UserRepository
from ..schemas.UserSchemas import *
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from ..models.UserModel import User
from ..specifications.UserSpecifications import UserSpecification
from sqlalchemy.ext.asyncio import AsyncSession


async def user_exist(user: CreateUserSchema, db: AsyncSession, user_id=None):
    results = await UserRepository(db).filter_by_spec((UserSpecification.existing_email(user.email) |
                                                      UserSpecification.existing_username(user.username))
                                                     & ~UserSpecification.is_deleted()
                                                     & ~UserSpecification.id_is(user_id))
    return len(results)


async def check_login_and_password(user: LoginUserSchema, db: AsyncSession):
    return await UserRepository(db).filter_by_spec(UserSpecification.existing_password(user.password) &
                                                   UserSpecification.existing_username(user.username) & ~UserSpecification.is_deleted())


async def register_user(user: CreateUserSchema, db: AsyncSession):
    if await user_exist(user, db):
        raise HTTPException(status_code=400, detail="Данный пользователь существует")
    user_id = uuid.uuid4()

    new_user = User(
        user_id=user_id,
        email=user.email,
        username=user.username,
        password=user.password,
        sex=user.sex,
        image_url=str(user.image_url) if user.image_url else None,
        is_deleted=False
    )

    await UserRepository(db).add(new_user)
    access_token = create_access_token(str(user_id))

    return {"access_token": access_token}


async def authorize_user(user: LoginUserSchema, db: AsyncSession):
    user_data = await check_login_and_password(user, db)
    if user_data:
        access_token = create_access_token(str(user_data[0].user_id))
        return {"access_token": access_token}
    else:
        raise HTTPException(status_code=400, detail="Неправильно введён логин или пароль")


async def get_users_info(user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    users_info = await UserRepository(db).filter_by_spec(~UserSpecification.is_deleted()
                                                         & UserSpecification.id_is(user_token.sub))

    if not users_info:
        raise HTTPException(status_code=404, detail="Пользователь не найден или удалён")

    return {"data": UserResponseSchema.model_validate(users_info[0]).model_dump()}


async def update_users_info(updated_user: CreateUserSchema, user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    user_id = user_token.sub

    if await user_exist(updated_user, db, user_id):
        raise HTTPException(status_code=400, detail="Данный пользователь существует")

    new_user = {
        "user_id": user_id,
        "email": updated_user.email,
        "username": updated_user.username,
        "password": updated_user.password,
        "sex": updated_user.sex,
        "image_url": str(updated_user.image_url) if updated_user.image_url else None
    }
    await UserRepository(db).update(new_user)
    return {"status": "updated"}


async def delete_user(user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    user_id = user_token.sub
    user = {
        "user_id": user_id,
        "is_deleted": True
    }
    await UserRepository(db).update(user)
    return {"status": "deleted"}
