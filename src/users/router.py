import os
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import insert
from starlette import status

from src.products.dependencies import DbDep, bcrypt_context
from src.products.models import User
from src.users.schemas import CreateUser
from src.users.service import authenticate_user, create_access_token

users_router = APIRouter(prefix='/users', tags=['users'])


@users_router.post("/", response_model=CreateUser, status_code=201)
async def create_user(create_user: CreateUser, db: DbDep):
    await db.execute(insert(User).values(
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        password_hash=bcrypt_context.hash(create_user.password),
        username=create_user.username,
    ))
    await db.commit()

    return create_user


@users_router.post('/token')
async def login(db: DbDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate user'
        )

    token = await create_access_token(user.username, user.id, user.is_admin,
                                      expires_delta=timedelta(minutes=int(os.getenv('TOKEN_LIFETIME'))))
    return {
        'access_token': token,
        'token_type': 'bearer'
    }