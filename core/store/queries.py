from typing import List

from sqlalchemy import and_, select
from sqlalchemy.orm import aliased

from core.queries import Query
from core.store.models import Category, Item, Discount, Order
from core.store.schemas import ItemResponse, ItemListFilter, CategoryResponse, CategoryBase, DiscountBase, OrderFilter


class ItemQuery(Query):

    async def items(self, list_filter: ItemListFilter) -> List[ItemResponse]:
        category_id = list_filter.category_id
        category_cte = None

        if category_id:
            category_alias = aliased(Category)

            # CTE: Recursive query to fetch the category and its subcategories
            category_cte = select(Category.id).where(Category.id == category_id).cte(recursive=True)

            category_cte = category_cte.union_all(
                select(category_alias.id).where(category_alias.parent_id == category_cte.c.id),
            )

        q = select(Item)

        where_conditions = []

        if list_filter and list_filter.only_available:
            where_conditions.append(Item.stock > 0)
        if category_id:
            q = q.join(Category, Item.category_id == Category.id)
            where_conditions.append(
                Category.id.in_(select(category_cte.c.id)),
            )

        q = q.where(and_(*where_conditions))

        if list_filter:
            q = q.limit(list_filter.limit).offset(list_filter.offset)

        resp = await self.db.execute(q)
        items = resp.scalars().all()
        cat_ids = [i.category_id for i in items]
        q = select(Discount).where(Discount.category_id.in_(cat_ids), Discount.is_active.is_(True))
        discounts = await self._execute_all(q)
        return self._serialize(items, discounts)

    def _serialize(self, items: List[Item], discounts: List[Discount]) -> List[ItemResponse]:
        discount_map = {d.category_id: d for d in discounts}
        data = [
            ItemResponse(
                id=i.id,
                price=i.price,
                stock=i.stock,
                name=str(i.name),
                category=CategoryBase(
                    id=i.category_id,
                    name=i.category.name,
                ),
                discount=(
                    DiscountBase(
                        id=discount_map[i.category_id].id,
                        value=discount_map[i.category_id].value,
                    )
                    if discount_map.get(i.category_id)
                    else None
                ),
            )
            for i in items
        ]
        return data


class CategoryQuery(Query):

    async def categories(self) -> List[CategoryResponse]:
        q = select(Category)
        categories = await self._execute_all(q)
        return self._build_category_tree(categories)

    def _build_category_tree(
        self,
        categories: List[Category] = None,
        parent_id: int = None,
    ) -> List[CategoryResponse]:
        tree = []
        for category in categories:
            if category.parent_id == parent_id:
                children = self._build_category_tree(categories, category.id)
                tree.append(CategoryResponse(id=category.id, name=category.name, children=children))
        return tree


class DiscountQuery(Query):

    async def discounts(self) -> List[Discount]:
        q = select(Discount)
        return await self._execute_all(q)


class OrderQuery(Query):

    async def orders(self, list_filter: OrderFilter) -> List[Order]:
        q = select(Order).outerjoin(Item)

        where_conditions = []
        if list_filter.item_id:
            where_conditions.append(Order.item_id == list_filter.item_id)
        if list_filter.category_id:
            where_conditions.append(Item.category_id == list_filter.category_id)
        if list_filter.status:
            where_conditions.append(Order.status == list_filter.status)

        q = q.where(*where_conditions).limit(list_filter.limit).offset(list_filter.offset)

        return await self._execute_all(q)
