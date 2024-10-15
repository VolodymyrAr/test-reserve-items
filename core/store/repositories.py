from sqlalchemy import update, select, exists

from core.repositories import Repository
from core.store.enums import OrderStatus
from core.store.models import Category, Item, Discount, Order


class CategoryRepository(Repository[Category]):
    model = Category


class ItemRepository(Repository[Item]):
    model = Item

    async def allow_delete(self, item_id: int) -> bool:
        q = select(exists().where(Order.item_id == item_id, Order.status == OrderStatus.RESERVED))
        resp = await self._execute(q)
        return not resp.scalar()


class DiscountRepository(Repository[Discount]):
    model = Discount

    async def get_active(self, category_id: int) -> Discount:
        q = select(Discount).where(Discount.category_id == category_id, Discount.is_active.is_(True))
        return await self._execute_one(q)

    async def deactivate_for_category(self, category_id: int) -> None:
        q = (
            update(Discount)
            .where(Discount.category_id == category_id, Discount.is_active.is_(True))
            .values({Discount.is_active: False})
        )
        await self._execute(q)


class OrderRepository(Repository[Order]):
    model = Order
