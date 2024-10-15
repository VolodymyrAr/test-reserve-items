from typing import Optional, List
from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

from core.mixins import ExecuteMixin

T = TypeVar("T", bound=DeclarativeMeta)


class Repository(ExecuteMixin, Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        q = select(self.model).where(self.model.id == obj_id)
        return await self._execute_one(q)

    async def list_by_ids(self, ids: List[int]) -> List[T]:
        q = select(self.model).where(self.model.id.in_(ids))
        return await self._execute_all(q)
