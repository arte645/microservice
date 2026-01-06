from types import CoroutineType
from typing import Any
from authx import TokenPayload
from ..repositories.UserRepository import UserRepository
from ..repositories.SubscriptionsRepository import SubscriptionRepository
from ..schemas.UserSchemas import *
from .AuthorizationController import *
from fastapi import HTTPException
import uuid
from ..models.UserModel import User
from ..models.SubscriptionsModel import Subscription
from ..specifications.UserSpecifications import UserSpecification
from ..specifications.SubscriptionSpecifications import SubscriptionSpecification
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

async def subscribe_to_user(target_user_id: str, user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    subscriber_user_id = user_token.sub

    if subscriber_user_id == target_user_id:
        raise HTTPException(status_code=400, detail="Нельзя подписаться на самого себя")

    target_user = await UserRepository(db).filter_by_spec(~UserSpecification.is_deleted()
                                                          & UserSpecification.id_is(target_user_id))
    if not target_user:
        raise HTTPException(status_code=404, detail="Пользователь, на которого вы пытаетесь подписаться, не найден")
    
    existing_subscription = await SubscriptionRepository(db).filter_by_spec(
        SubscriptionSpecification.subscriber_user_id_is(subscriber_user_id) &
        SubscriptionSpecification.target_user_id_is(target_user_id))
    
    if existing_subscription:
        return {"status": f"Already subscribed to user {target_user_id}"}
    
    await SubscriptionRepository(db).add(Subscription(
        subscriber_user_id=subscriber_user_id,
        target_user_id=target_user_id
    ))
    return {"status": f"Subscribed to user {target_user_id}"}

async def subscription_key(subscription_key: str, user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    user_id = user_token.sub

    user = await UserRepository(db).filter_by_spec(~UserSpecification.is_deleted()
                                                  & UserSpecification.id_is(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден или удалён")

    new_user = {
        "user_id": user_id,
        "subscription_key": subscription_key
    }
    await UserRepository(db).update(new_user)
    return {"status": "subscription key updated"}

async def get_all_users(db: AsyncSession):
    all_users = await UserRepository(db).filter_by_spec(~UserSpecification.is_deleted())
    return {"data": [UserListResponseSchema.model_validate(c).model_dump() for c in all_users]}

async def get_all_my_subscriptions(user_token: CoroutineType[Any, Any, TokenPayload], db: AsyncSession):
    user_id = user_token.sub
    all_subs = await  SubscriptionRepository(db).filter_by_spec(SubscriptionSpecification.target_user_id_is(user_id))
    return {"data": [s.target_user_id for s in all_subs]}
