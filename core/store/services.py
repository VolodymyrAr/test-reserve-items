from typing import List

from core.exceptions import ObjNotFoundError
from core.services import Service
from core.store.models import Item, Category
from core.store.schemas import ItemListFilter, CategoryCreate, CategoryTreeResponse, ItemCreate, ItemUpdate


class CategoryNotFound(ObjNotFoundError):
    pass


class ItemNotFound(ObjNotFoundError):
    pass


class CategoryService(Service):

    async def create(self, category_data: CategoryCreate) -> Category:
        category = Category(
            name=category_data.name,
            parent_id=category_data.parent_id,
        )
        await self.uow.categories.add(category)
        return category

    async def get_list(self) -> List[Category]:
        categories = await self.uow.categories.get_all()
        return categories

    async def build_category_tree(
        self,
        categories: List[Category] = None,
        parent_id: int = None,
    ) -> List[CategoryTreeResponse]:
        tree = []
        for category in categories:
            if category.parent_id == parent_id:
                children = await self.build_category_tree(categories, category.id)
                tree.append(CategoryTreeResponse(id=category.id, name=category.name, children=children))
        return tree


class ItemService(Service):

    async def get_list(self, list_filter: ItemListFilter) -> List[Item]:
        items = await self.uow.items.get_all(list_filter)
        return items

    async def create(self, item_data: ItemCreate) -> Item:
        category = await self.uow.categories.get_by_id(item_data.category_id)
        if not category:
            raise CategoryNotFound(f"Category id:{item_data.category_id} not found")

        item = Item(
            name=item_data.name,
            price=item_data.price,
            category_id=item_data.category_id,
            stock=item_data.stock,
        )
        return await self.uow.items.add(item)

    async def update(self, item_id: int, item_data: ItemUpdate) -> Item:
        item = await self.uow.items.get_by_id(item_id)
        if not item:
            raise ItemNotFound(f"Item id:{item_id} not found")

        item.price = item_data.price or item.price
        item.stock = item_data.stock or item.stock
        return item
