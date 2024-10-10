from typing import Optional, List
from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class Repository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        q = select(self.model).where(self.model.id == obj_id)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def add(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.flush()
        await self.db.refresh(obj)
        return obj

    async def get_all(self, query_filter: BaseModel = None) -> List[T]:  # pylint: disable=unused-argument
        q = select(self.model)
        res = await self.db.execute(q)
        return res.scalars().all()
