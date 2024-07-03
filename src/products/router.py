from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.products.schemas import ProductSchema
from src.database import get_db
from src.products.models import Product

products_router = APIRouter()


@products_router.get('/{product_id}')
async def get_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if not product:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product


@products_router.post('/create')
async def create_product(product_data: ProductSchema, db: Annotated[AsyncSession, Depends(get_db)]):
    await db.execute(insert(Product).values(name=product_data.name,
                                            description=product_data.description,
                                            price=product_data.price,
                                            availability=product_data.availability,
                                            category_id=product_data.category_id))
    await db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@products_router.put('/{product_id}')
async def update_product(product_id: int, product_data: ProductSchema, db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар с данным id не найден'
        )
    await db.execute(update(Product).where(Product.id == product_id).values(name=product_data.name,
                                                                            description=product_data.description,
                                                                            price=product_data.price,
                                                                            availability=product_data.availability,
                                                                            category_id=product_data.category_id))
    await db.commit()
    return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Данные о товаре успешно обновлены'
        }


@products_router.delete('/{product_id}')
async def delete_product(product_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    product = await db.scalar(select(Product).where(Product.id == product_id))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товар с данным id не найден'
        )
    await db.execute(delete(Product).where(Product.id == product_id))
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Товар успешно удален'
    }

