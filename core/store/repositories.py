from typing import List

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from core.repositories import Repository
from core.schemas import Pagination
from core.store.entities import Item, Category
from core.store.models import ItemModel, CategoryModel
from core.store.schemas import ItemListFilter, CategoryCreate
from core.store.utils import get_category_cte


class CategoryRepository(Repository):

    async def create(self, data: CategoryCreate) -> Category:
        db_category = CategoryModel(
            name=data.name,
            parent_id=data.parent_id,
        )
        self.db.add(db_category)
        await self.db.flush()
        return self._map_to_domain(db_category)

    async def get_all(self, list_filter: Pagination) -> List[Category]:
        q = (
            select(CategoryModel)
            .where(CategoryModel.parent_id.is_(None))
            .limit(list_filter.limit)
            .offset(list_filter.offset)
        )
        resp = await self.db.execute(q)
        db_categories = resp.scalars().all()
        ids = [cat.id for cat in db_categories]
        print("== HERE ==", ids)
        category_cte = get_category_cte(ids)
        q = select(CategoryModel).where(CategoryModel.id.in_(select(category_cte.c.id)))
        resp = await self.db.execute(q)
        db_categories = resp.scalars().all()
        print("== HERE ==", db_categories)
        return self._build_category_tree(db_categories)

    def _build_category_tree(
        self,
        categories: List[CategoryModel] = None,
        parent_id: int = None,
    ) -> List[Category]:
        tree = []
        for category in categories:
            if category.parent_id == parent_id:
                children = self._build_category_tree(categories, category.id)
                tree.append(Category(id=category.id, name=category.name, children=children))
        return tree

    def _map_to_domain(self, db_category: CategoryModel) -> Category:
        category = Category(
            id=db_category.id,
            name=db_category.name,
        )
        return category


class ItemRepository(Repository):

    async def add(self, obj: ItemModel) -> Item:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj, attribute_names=["category"])
        return obj

    async def get_by_id(self, obj_id: int) -> Item:
        q = select(ItemModel).options(joinedload(ItemModel.category)).where(ItemModel.id == obj_id)
        resp = await self.db.execute(q)
        return resp.scalar_one_or_none()

    async def get_all(self, query_filter: ItemListFilter = None) -> List[Item]:
        category_id = query_filter.category_id
        category_cte = None

        if category_id:
            category_cte = get_category_cte([category_id])

        q = select(ItemModel).options(joinedload(ItemModel.category))

        where_conditions = []

        if query_filter and query_filter.only_available:
            where_conditions.append(ItemModel.stock > 0)
        if category_id:
            q = q.join(CategoryModel, ItemModel.category_id == CategoryModel.id)
            where_conditions.append(
                CategoryModel.id.in_(select(category_cte.c.id)),
            )

        q = q.where(and_(*where_conditions))

        if query_filter:
            q = q.limit(query_filter.limit).offset(query_filter.offset)

        resp = await self.db.execute(q)
        return resp.scalars().all()
