# pylint: disable=unused-argument
from typing import List

from fastapi import APIRouter, Depends

from core.orders.schemas import ItemListFilter, CategoryCreate, CategoryResponse
from core.orders.services import CategoryService
from core.uow import UnitOfWork, get_uow
from core.users.models import User
from core.users.services import get_user, get_superuser

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
async def get_categories_list(user: User = Depends(get_user), uow: UnitOfWork = Depends(get_uow)):
    srv = CategoryService(uow)
    return await srv.get_list()


@router.post("/categories", response_model=CategoryResponse)
async def create_category(req: CategoryCreate, user: User = Depends(get_superuser), uow: UnitOfWork = Depends(get_uow)):
    srv = CategoryService(uow)
    return srv.create(req)


@router.get("/items")
async def items_list(
    query: ItemListFilter = Depends(),
    user: User = Depends(get_user),
):
    raise NotImplementedError


@router.get("/report")
async def sell_report(
    user: User = Depends(get_superuser),
):
    raise NotImplementedError


orders = router
