from fastapi import HTTPException
from starlette import status


def no_product_error():
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар с данным id не найден'
        )


def no_category_error():
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Категория с данным id не найдена'
        )