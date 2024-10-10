from pydantic import BaseModel

from core.schemas import Pagination


class ItemListFilter(Pagination):
    only_available: bool = True


class ItemCreate(BaseModel):
    name: str
    price: int
    category_id: str
    stock: int = 0


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
    parent_id: int


class CategoryResponse(BaseModel):
    id: int
    name: str
    children: list["CategoryResponse"]
