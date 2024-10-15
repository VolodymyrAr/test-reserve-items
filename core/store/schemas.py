from typing import List, Optional

from pydantic import BaseModel

from core.schemas import Pagination
from core.store.enums import OrderStatus


class ItemListFilter(Pagination):
    only_available: bool = True
    category_id: Optional[int] = None


class OrderFilter(Pagination):
    status: OrderStatus = OrderStatus.RESERVED
    item_id: Optional[int] = None
    category_id: Optional[int] = None


class CategoryBase(BaseModel):
    id: int
    name: str


class DiscountCreate(BaseModel):
    category_id: int
    value: int


class DiscountBase(BaseModel):
    id: int
    value: int


class DiscountResponse(DiscountBase):
    is_active: bool
    category: CategoryBase


class ItemCreate(BaseModel):
    name: str
    price: int
    category_id: int
    stock: int = 0


class ItemUpdate(BaseModel):
    price: Optional[int] = None
    stock: Optional[int] = None


class CategoryCreate(BaseModel):
    name: str
    parent_id: int = None


class CategoryResponse(CategoryBase):
    children: List["CategoryResponse"] = []


class ItemResponse(BaseModel):
    id: int
    price: int
    name: str
    discount: Optional[DiscountBase] = None
    category: CategoryBase
    stock: int


class OrderResponse(BaseModel):
    id: int
    item_id: Optional[int] = None
    status: OrderStatus
    name: str
    price: int
    discount: Optional[int] = None
    quantity: int


class OrderCreate(BaseModel):
    quantity: int
