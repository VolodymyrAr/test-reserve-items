from typing import List, Optional

from pydantic import BaseModel

from core.schemas import Pagination


class ItemListFilter(Pagination):
    only_available: bool = True
    category_id: Optional[int] = None


class ItemCreate(BaseModel):
    name: str
    price: int
    category_id: int
    stock: int = 0


class ItemUpdate(BaseModel):
    price: Optional[int] = None
    stock: Optional[int] = None


class ItemCategoryResponse(BaseModel):
    id: int
    name: str


class ItemResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    category: ItemCategoryResponse


class CategoryCreate(BaseModel):
    name: str
    parent_id: int = None


class CategoryResponse(BaseModel):
    id: int
    name: str


class CategoryTreeResponse(CategoryResponse):
    children: List["CategoryTreeResponse"] = []
