import uuid
from typing import List, Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship, backref

from src.users.schemas import UserSchema


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, index=True)


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    slug:Mapped[str] = mapped_column(unique=True, index=True)
    products: Mapped[List["Product"]] = relationship(back_populates="category", lazy="selectin")
    # parent_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    availability: Mapped[bool] = mapped_column()
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('category.id'), nullable=True)
    category: Mapped["Category"] = relationship(back_populates="products")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    username: Mapped[str| None] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column(default=False)

    def to_read_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            password=self.password_hash,
            is_admin=self.is_admin
        )

