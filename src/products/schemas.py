from typing import Union, Optional

from pydantic import BaseModel, EmailStr


class BaseProductSchema(BaseModel):
    name: str
    description: str
    price: int
    availability: bool
    category_id: Optional[int] = None



class ProductSchema(BaseProductSchema):
    id: int

    class Config:
        from_attributes = True


class CreateProductSchema(BaseProductSchema):
    pass


class BaseCategorySchema(BaseModel):
    name: str


class CategorySchema(BaseModel):
    id: int
    products: list[ProductSchema] | None = None

class CreateCategorySchema(BaseCategorySchema):
    pass




