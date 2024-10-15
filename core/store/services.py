from sqlalchemy.orm import lazyload

from core.exceptions import ObjNotFoundError, NotAllowed, ServiceError
from core.services import Service
from core.store.enums import OrderStatus
from core.store.models import Category, Item, Discount, Order
from core.store.schemas import CategoryCreate, ItemCreate, ItemUpdate, DiscountCreate


class CategoryNotFound(ObjNotFoundError):
    pass


class ItemNotFound(ObjNotFoundError):
    pass


class OrderNotFound(ObjNotFoundError):
    pass


class ItemStockNotEnough(ServiceError):
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
            name=item_data.name,
        )
        return await self.uow.items.add(item)

    async def update(self, item_id: int, item_data: ItemUpdate) -> Item:
        item = await self.uow.items.get_by_id(item_id)
        if not item:
            raise ItemNotFound(f"Item id:{item_id} not found")

        item.price = item_data.price or item.price
        item.stock = item_data.stock or item.stock
        return item

    async def delete(self, item_id: int):
        if not await self.uow.items.allow_delete(item_id):
            raise NotAllowed("Item id:{item_id} cannot be deleted")
        await self.uow.items.delete(item_id)


class DiscountService(Service):

    async def create(self, data: DiscountCreate) -> Discount:
        discount = Discount(
            value=data.value,
            category_id=data.category_id,
            is_active=False,
        )
        return await self.uow.discounts.add(discount)

    async def activate(self, discount_id: int) -> None:
        discount = await self.uow.discounts.get_by_id(discount_id)
        await self.uow.discounts.deactivate_for_category(discount_id)
        discount.is_active = True

    async def deactivate(self, discount_id: int) -> None:
        discount = await self.uow.discounts.get_by_id(discount_id)
        discount.is_active = False


class OrderService(Service):

    async def reserve_item(self, item_id: int, quantity: int, user_id: int) -> Order:
        item = await self.uow.items.get_by_id(item_id, for_update=True, options=[lazyload(Item.category)])

        if not item:
            raise ItemNotFound(f"Item id:{item_id} not found")

        discount = await self.uow.discounts.get_active(item.category_id)
        item.stock -= quantity

        if item.stock <= 0:
            raise ItemStockNotEnough("Not enough stock for item_id:{item_id}")

        order = Order(
            user_id=user_id,
            item_id=item_id,
            name=str(item.name),
            price=item.price,
            discount=discount.value if discount else None,
            status=OrderStatus.RESERVED,
            quantity=quantity,
        )
        await self.uow.orders.add(order)
        return order

    async def cancel_order(self, order_id: int) -> None:
        order = await self.uow.orders.get_by_id(order_id)

        item = await self.uow.items.get_by_id(order.item_id, for_update=True, options=[lazyload(Item.category)])
        item.stock += order.quantity
        order.status = OrderStatus.CANCELLED

    async def confirm_order(self, order_id: int) -> None:
        order = await self.uow.orders.get_by_id(order_id)

        if not order:
            raise OrderNotFound(f"Order id:{order_id} not found")

        if not order.status == OrderStatus.RESERVED:
            raise NotAllowed(f"Order id:{order_id} cannot be cancelled")

        order.status = OrderStatus.SOLD
