from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload
from slugify import slugify
from src.products.models import Product, Category


async def get_products_repository(db, skip, limit):
    query = select(Product).offset(skip).limit(limit)
    result = await db.execute(query)
    products = result.scalars().all()
    return products


async def search_product_repository(name, db, skip, limit):
    query = select(Product).offset(skip).limit(limit).where(Product.name == name)
    result = await db.execute(query)
    products = result.scalars().all()
    return products


# async def create_product_repository(product_data, db):
#     await db.execute(insert(Product).values(name=product_data.name,
#                                             description=product_data.description,
#                                             price=product_data.price,
#                                             availability=product_data.availability,
#                                             category_id=product_data.category_id))
#     await db.commit()

async def create_product_repository(product_data, db):
    product = Product(**product_data.model_dump())
    db.add(product)
    await db.commit()


async def select_product_repository(product_id, db):
    result = await db.scalar(select(Product).where(Product.id == product_id))
    return result


async def delete_product_repository(product_id, db):
    await db.execute(delete(Product).where(Product.id == product_id))
    await db.commit()


async def update_product_repository(product_id, product_data, db):
    query = update(Product).where(Product.id == product_id).values(name=product_data.name,
                                                                   description=product_data.description,
                                                                   price=product_data.price,
                                                                   availability=product_data.availability,
                                                                   category_id=product_data.category_id)
    await db.execute(query)
    await db.commit()


async def get_categories_repository(db, skip, limit):
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    categories = result.scalars().all()
    return categories


async def create_category_repository(db, create_category):
    await db.execute(insert(Category).values(name=create_category.name,
                                             slug=slugify(create_category.name)))
    await db.commit()


async def select_category_repository(category_id, db):
    result = await db.scalar(select(Category).where(Category.id == category_id))
    return result


async def category_slug_repository(db, category_slug):
    category = await db.scalar(select(Category).where(Category.slug == category_slug))
    return category


async def get_subcategories_repository(db, category):
    subcategories = await db.scalars(select(Category).where(Category.parent_id == category.id))
    return subcategories





async def update_category_repository(db, category_id, update_category):
    query = update(Category).where(Category.id == category_id).values(name=update_category.name,
                                                                      parent_id=update_category.parent_id)
    await db.execute(query)
    await db.commit()