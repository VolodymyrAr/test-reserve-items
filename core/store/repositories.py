from typing import List

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload, aliased

from core.repositories import Repository
from core.store.models import Item, Category
from core.store.schemas import ItemListFilter


class CategoryRepository(Repository[Category]):
    model = Category


class ItemRepository(Repository[Item]):
    model = Item

    async def add(self, item: Item) -> Item:  # pylint: disable=arguments-renamed
        self.db.add(item)
        await self.db.flush()
        await self.db.refresh(item, attribute_names=["category"])
        return item

    async def get_by_id(self, item_id: int) -> Item:  # pylint: disable=arguments-renamed
        q = select(Item).options(joinedload(Item.category)).where(Item.id == item_id)
        resp = await self.db.execute(q)
        return resp.scalar_one_or_none()

    async def get_all(self, query_filter: ItemListFilter = None) -> List[Item]:
        category_id = query_filter.category_id
        category_cte = None

        if category_id:
            category_alias = aliased(Category)

            # CTE: Recursive query to fetch the category and its subcategories
            category_cte = select(Category.id).where(Category.id == category_id).cte(recursive=True)

            category_cte = category_cte.union_all(
                select(category_alias.id).where(category_alias.parent_id == category_cte.c.id),
            )

        q = select(Item).options(joinedload(Item.category))

        where_conditions = []

        if query_filter and query_filter.only_available:
            where_conditions.append(Item.stock > 0)
        if category_id:
            q = q.join(Category, Item.category_id == Category.id)
            where_conditions.append(
                Category.id.in_(select(category_cte.c.id)),
            )

        q = q.where(and_(*where_conditions))

        if query_filter:
            q = q.limit(query_filter.limit).offset(query_filter.offset)

        resp = await self.db.execute(q)
        return resp.scalars().all()
