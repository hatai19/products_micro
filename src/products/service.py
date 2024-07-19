from sqlalchemy.ext.asyncio import AsyncSession

from src.products.exceptions import no_product_error, no_category_error
from src.products.repositories import select_product_repository, update_product_repository, delete_product_repository, \
    select_category_repository, update_category_repository, category_slug_repository
from src.products.schemas import ProductSchema


async def get_product_service(product_id, db):
    product = await select_product_repository(product_id, db)
    if product is None:
        no_product_error()
    return product


async def update_product_service(product_id, product_data, db):
    product = await select_product_repository(product_id, db)
    if product is None:
        no_product_error()

    await update_product_repository(product_id, product_data, db)


async def delete_product_service(product_id, db):
    product = await select_product_repository(product_id, db)
    if product is None:
        no_product_error()
    await delete_product_repository(product_id, db)


async def get_category_service(category_id, db):
    category = await select_category_repository(category_id, db)
    if category is None:
        no_category_error()
    return category


async def update_category_service(db, category_id, update_category):
    category = await select_category_repository(category_id, db)
    if category is None:
        no_category_error()
    await update_category_repository(db, category_id, update_category)

