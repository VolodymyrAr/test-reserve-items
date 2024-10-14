from typing import List

from core.exceptions import ObjNotFoundError
from core.schemas import Pagination
from core.services import Service
from core.store.entities import Item, Category
from core.store.models import ItemModel
from core.store.schemas import ItemListFilter, CategoryCreate, ItemCreate, ItemUpdate


class CategoryNotFound(ObjNotFoundError):
    pass


class ItemNotFound(ObjNotFoundError):
    pass


class CategoryService(Service):

    async def create(self, data: CategoryCreate) -> Category:
        category = await self.uow.categories.create(data)
        return category

    async def get_list(self, list_filter: Pagination) -> List[Category]:
        categories = await self.uow.categories.get_all(list_filter)
        return categories


class ItemService(Service):

    async def get_list(self, list_filter: ItemListFilter) -> List[Item]:
        items = await self.uow.items.get_all(list_filter)
        return items

    async def create(self, item_data: ItemCreate) -> ItemModel:
        category = await self.uow.categories.get_by_id(item_data.category_id)
        if not category:
            raise CategoryNotFound(f"Category id:{item_data.category_id} not found")

        item = ItemModel(
            name=item_data.name,
            price=item_data.price,
            category_id=item_data.category_id,
            stock=item_data.stock,
        )
        return await self.uow.items.add(item)

    async def update(self, item_id: int, item_data: ItemUpdate) -> ItemModel:
        item = await self.uow.items.get_by_id(item_id)
        if not item:
            raise ItemNotFound(f"Item id:{item_id} not found")

        item.price = item_data.price or item.price
        item.stock = item_data.stock or item.stock
        return item
