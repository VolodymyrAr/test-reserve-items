from typing import List

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import aliased

from core.store.models import CategoryModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_category_cte(ids: List[int]):
    category_alias = aliased(CategoryModel)

    # CTE: Recursive query to fetch the category and its subcategories
    category_cte = select(CategoryModel.id).where(CategoryModel.id.in_(ids)).cte(recursive=True)
    category_cte = category_cte.union_all(
        select(category_alias.id).where(category_alias.parent_id == category_cte.c.id),
    )
    return category_cte


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password) -> str:
    return pwd_context.hash(password)
