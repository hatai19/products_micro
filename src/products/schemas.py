from typing import Union

from pydantic import BaseModel


class ProductSchema(BaseModel):
    name: str
    description: str
    price: int
    availability: bool
    category_id: Union[int, None] = None

