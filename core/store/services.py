from core.exceptions import ObjNotFoundError
from core.services import Service
from core.store.models import Category, Item, Discount
from core.store.schemas import CategoryCreate, ItemCreate, ItemUpdate, DiscountCreate


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


class ItemService(Service):

    async def create(self, item_data: ItemCreate) -> Item:
        category = await self.uow.categories.get_by_id(item_data.category_id)
        if not category:
            raise CategoryNotFound(f"Category id:{item_data.category_id} not found")
        item = Item(
            price=item_data.price,
            stock=item_data.stock,
            category_id=category.id,
        )
        return await self.uow.items.add(item)

    async def update(self, item_id: int, item_data: ItemUpdate) -> Item:
        item = await self.uow.items.get_by_id(item_id)
        if not item:
            raise ItemNotFound(f"Item id:{item_id} not found")

        item.price = item_data.price or item.price
        item.stock = item_data.stock or item.stock
        return item


class DiscountService(Service):

    async def create(self, data: DiscountCreate) -> Discount:
        discount = Discount(
            value=data.value,
            category_id=data.category_id,
            is_active=False,
        )
        return await self.uow.discounts.add(discount)

    async def activate(self, discount_id: int) -> None:
        await self.uow.discounts.activate(discount_id)

    async def deactivate(self, discount_id: int) -> None:
        discount = await self.uow.discounts.get_by_id(discount_id)
        discount.is_active = False
