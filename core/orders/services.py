from typing import List

from core.services import Service
from core.orders.models import Item, Category
from core.orders.schemas import ItemListFilter, CategoryCreate


class CategoryService(Service):

    async def create(self, category_data: CategoryCreate) -> Category:
        category = Category(
            name=category_data.name,
            parent_id=category_data.parent_id,
        )
        await self.uow.categories.add(category)
        return category

    async def get_list(self) -> List[Category]:
        return await self.uow.categories.get_all()


class ItemService(Service):

    async def get_list(self, list_filter: ItemListFilter) -> List[Item]:
        items = await self.uow.items.get_all(list_filter)
        return items

    # async def create(self, item_data: ItemCreate) -> Item:
    #     item = Item(name=name, price=price, category_id=category_id)
