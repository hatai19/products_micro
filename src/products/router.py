from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from src.products.dependencies import DbDep, bcrypt_context
from src.products.exceptions import no_product_error
from src.products.repositories import create_product_repository, select_product_repository, get_products_repository, \
    get_categories_repository, create_category_repository, search_product_repository
from src.products.schemas import ProductSchema, CreateProductSchema, CreateCategorySchema, CategorySchema
from src.database import get_db
from src.products.models import Product, Category
from src.products.service import update_product_service, delete_product_service, get_product_service, \
    get_category_service, update_category_service
from src.users.service import get_current_user

products_router = APIRouter(prefix='/products', tags=['products'])
categories_router = APIRouter(prefix='/categories', tags=['categories'])


@categories_router.get('/', response_model=List[CategorySchema])
async def get_all_categories(db: DbDep, skip: int = 0, limit: int = 10):
    categories = await get_categories_repository(db, skip, limit)
    return categories


@categories_router.get('/detail/{category_id}', response_model=CategorySchema)
async def get_category(category_id: int, db: DbDep):
    result = await get_category_service(category_id, db)
    return result


@categories_router.post('/create') #response_model=CreateCategorySchema)
async def create_category(db: DbDep, create_category: CreateCategorySchema, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        await create_category_repository(db, create_category)
        #return create_category


@categories_router.put('/detail/{category_id}',response_model=CreateCategorySchema)
async def update_category(db: DbDep, category_id: int, update_category: CreateCategorySchema):
    await update_category_service(db, category_id, update_category)
    return update_category


@products_router.get("/" ,response_model=list[ProductSchema])
async def read_products(db: DbDep, skip: int = 0, limit: int = 10):
    products = await get_products_repository(db, skip, limit)
    return products


@products_router.get("/{name}", response_model=list[ProductSchema])
async def search_product_by_name(name: str, db: DbDep, skip: int = 0, limit: int = 10):
    result = await search_product_repository(name, db, skip, limit)
    return result


@products_router.get("/detail/{product_id}", response_model=ProductSchema)
async def get_product(product_id: int, db: DbDep):
    result = await get_product_service(product_id, db)
    return result


@products_router.post('/create', response_model=CreateProductSchema)
async def create_product(product_data: CreateProductSchema, db: DbDep):
    await create_product_repository(product_data, db)
    product_data.model_dump()
    return product_data


@products_router.put('/detail/{product_id}', response_model=CreateProductSchema)
async def update_product(product_id: int, product_data: CreateProductSchema, db: DbDep):
    await update_product_service(product_id, product_data, db)
    return product_data


@products_router.delete('/detail/{product_id}')
async def delete_product(product_id: int, db: DbDep):
    await delete_product_service(product_id, db)
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Товар успешно удален'
    }


@products_router.get("/{category_slug}",response_model=List[ProductSchema])
async def product_by_category(category_slug: str, db: DbDep):
    category = db.query(Category).filter(Category.slug == category_slug).first()

    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")

    products = db.query(Product).filter(Product.category_id == category.id).all()

    return products



