# pylint: disable=unused-argument
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.schemas import Pagination, ID, Action
from core.store.queries import CategoryQuery, DiscountQuery, ItemQuery
from core.store.schemas import (
    ItemListFilter,
    CategoryCreate,
    ItemCreate,
    ItemUpdate,
    CategoryResponse,
    DiscountResponse,
    DiscountCreate,
    ItemResponse,
)
from core.store.services import CategoryService, ItemService, DiscountService
from core.uow import UnitOfWork, get_uow
from core.users.models import User
from core.users.services import get_superuser

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories_list(db: AsyncSession = Depends(get_db)):
    return await CategoryQuery(db).categories()


@router.post("/categories", response_model=ID)
async def create_category(
    req: CategoryCreate,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = CategoryService(uow)
    return await srv.create(req)


@router.get("/discounts", response_model=List[DiscountResponse])
async def get_discounts(
    query: Pagination = Depends(), user: User = Depends(get_superuser), db: AsyncSession = Depends(get_db)
):
    return await DiscountQuery(db).discounts()


@router.post("/discounts", response_model=ID)
async def create_discount(
    req: DiscountCreate,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = DiscountService(uow)
    return await srv.create(req)


@router.post("/discounts/{discount_id}/activate", response_model=Action)
async def activate_discount(
    discount_id: int,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = DiscountService(uow)
    await srv.activate(discount_id)
    return Action(message="Discount activated")


@router.post("/discounts/{discount_id}/deactivate", response_model=Action)
async def deactivate_discount(
    discount_id: int,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = DiscountService(uow)
    await srv.deactivate(discount_id)
    return Action(message="Discount deactivated")


@router.get("/items", response_model=List[ItemResponse])
async def items_list(query: ItemListFilter = Depends(), db: AsyncSession = Depends(get_db)):
    return await ItemQuery(db).items(list_filter=query)


@router.post("/items", response_model=ID)
async def create_item(
    req: ItemCreate,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    return await srv.create(req)


@router.patch("/items/{item_id}")
async def update_item(
    item_id: int,
    req: ItemUpdate,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    await srv.update(item_id, req)
    return


store = router
