from typing import TypeVar, Generic, Type, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta
from uow import UnitOfWorkBase


T = TypeVar("T", bound=DeclarativeMeta)


class Repository(Generic[T]):
    model: Type[T]

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        q = select(self.model).where(id=obj_id)
        res = await self.db.execute(q)
        return res.scalar_one_or_none()

    async def add(self, obj: T) -> T:
        self.db.add(obj)
        await self.db.flush()
        return obj


class Service:

    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow
