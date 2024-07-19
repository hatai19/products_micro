import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from jose import jwt, JWTError
from src.products.dependencies import bcrypt_context, DbDep
from src.users.repository import select_user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
async def authenticate_user(db, username:str, password:str):
    user = await select_user_repository(db, username)
    if not user or not bcrypt_context.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные данные для аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def create_access_token(username: str, user_id: int, is_admin: bool, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'is_admin': is_admin}
    expires = datetime.now() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, os.getenv('SECRET_KEY'), algorithm=os.getenv('ALGORITHM'))


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                           db: DbDep):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[os.getenv('ALGORITHM')])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        expire = payload.get('exp')
        user = await select_user_repository(db, username)
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Не удалось подтвердить пользователя '
            )
        if expire is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Токен не был предоставлен"
            )
        if not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Недостаточно прав доступа'
            )
        return {
            'username': user.username,
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Не удалось подтвердить пользователя '
        )