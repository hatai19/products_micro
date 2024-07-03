from typing import List, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Category(Base):
    __tablename__ = "category"

    product: Mapped[List["Product"]] = relationship(back_populates="category")


class Product(Base):
    __tablename__ = "product"

    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    availability: Mapped[bool] = mapped_column()
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('category.id'))
    category: Mapped["Category"] = relationship(back_populates="product")

