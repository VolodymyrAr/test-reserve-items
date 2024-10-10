# pylint: disable=unused-argument
from typing import List

from fastapi import APIRouter, Depends

from core.store.schemas import (
    ItemListFilter,
    CategoryCreate,
    CategoryResponse,
    CategoryTreeResponse,
    ItemResponse,
    ItemCreate,
    ItemUpdate,
)
from core.store.services import CategoryService, ItemService
from core.uow import UnitOfWork, get_uow
from core.users.models import User
from core.users.services import get_user, get_superuser

router = APIRouter()


@router.get("/categories", response_model=List[CategoryTreeResponse])
async def get_categories_list(user: User = Depends(get_user), uow: UnitOfWork = Depends(get_uow)):
    srv = CategoryService(uow)
    categories = await srv.get_list()
    category_tree = await srv.build_category_tree(categories)
    return category_tree


@router.post("/categories", response_model=CategoryResponse)
async def create_category(req: CategoryCreate, user: User = Depends(get_superuser), uow: UnitOfWork = Depends(get_uow)):
    srv = CategoryService(uow)
    return await srv.create(req)


@router.get("/items", response_model=List[ItemResponse])
async def items_list(
    query: ItemListFilter = Depends(),
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    items = await srv.get_list(query)
    return items


@router.post("/items", response_model=ItemResponse)
async def create_item(
    req: ItemCreate,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    return await srv.create(req)


@router.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    req: ItemUpdate,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    item = await srv.update(item_id, req)
    return item


@router.get("/report")
async def sell_report(
    user: User = Depends(get_superuser),
):
    raise NotImplementedError


store = router
