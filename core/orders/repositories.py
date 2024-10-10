from typing import List

from sqlalchemy import select

from core.repositories import Repository
from core.orders.models import Item, Category
from core.orders.schemas import ItemListFilter


class CategoryRepository(Repository[Category]):
    model = Category


class ItemRepository(Repository[Item]):
    model = Item

    async def get_all(self, query_filter: ItemListFilter) -> List[Item]:
        q = select(Item)
        if query_filter.only_available:
            q = q.where(Item.stock > 0)
        q = q.limit(query_filter.limit).offset(query_filter.offset)
        resp = await self.db.execute(q)
        return resp.scalars().all()
