# pylint: disable=unused-argument
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.schemas import Pagination, ID, Action
from core.store.queries import CategoryQuery, DiscountQuery, ItemQuery, OrderQuery
from core.store.schemas import (
    ItemListFilter,
    CategoryCreate,
    ItemCreate,
    ItemUpdate,
    CategoryResponse,
    DiscountResponse,
    DiscountCreate,
    ItemResponse,
    OrderResponse,
    OrderCreate,
    OrderFilter,
)
from core.store.services import CategoryService, ItemService, DiscountService, OrderService
from core.uow import UnitOfWork, get_uow
from core.users.models import User
from core.users.services import get_superuser, get_user

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
    return Action(message="Item updated")


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    user: User = Depends(get_superuser),
    uow: UnitOfWork = Depends(get_uow),
):
    srv = ItemService(uow)
    await srv.delete(item_id)
    return Action(message="Item deleted")


@router.get("/orders", response_model=List[OrderResponse])
async def list_order(
    query: OrderFilter = Depends(), user: User = Depends(get_superuser), db: AsyncSession = Depends(get_db)
):
    return await OrderQuery(db).orders(list_filter=query)


@router.post("/items/{item_id}/reserve", response_model=ID)
async def reserve(
    item_id: int,
    req: OrderCreate,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
):
    """Create order for item with status reserved"""
    srv = OrderService(uow)
    return await srv.reserve_item(item_id, req.quantity, user.id)


@router.post("/orders/{order_id}/cancel", response_model=Action)
async def cancel_reserve(
    order_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
):
    """Create order for item with status reserved"""
    srv = OrderService(uow)
    await srv.cancel_order(order_id)
    return Action(message="Order cancelled")


@router.post("/orders/{order_id}/confirm", response_model=Action)
async def confirm_reserve(
    order_id: int,
    user: User = Depends(get_user),
    uow: UnitOfWork = Depends(get_uow),
):
    """Create order for item with status reserved"""
    srv = OrderService(uow)
    await srv.confirm_order(order_id)
    return Action(message="Order confirmed")


store = router
