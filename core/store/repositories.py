from sqlalchemy import update

from core.repositories import Repository
from core.store.models import Category, Item, Discount, Order, OrderItem


class CategoryRepository(Repository[Category]):
    model = Category


class ItemRepository(Repository[Item]):
    model = Item


class DiscountRepository(Repository[Discount]):
    model = Discount

    async def activate(self, discount_id: int) -> None:
        discount = await self.get_by_id(discount_id)
        q = (
            update(Discount)
            .where(Discount.id == discount_id, Discount.is_active.is_(True))
            .values({Discount.is_active: False})
        )
        await self._execute(q)
        discount.is_active = True


class OrderItemRepository(Repository[OrderItem]):
    model = OrderItem


class OrderRepository(Repository[Order]):
    model = Order
