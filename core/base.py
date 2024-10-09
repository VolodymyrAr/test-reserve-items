import abc
from abc import ABC
from typing import Optional
from typing import TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


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


class UnitOfWorkBase(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()
        await self.close()

    @abc.abstractmethod
    async def commit(self):
        pass

    @abc.abstractmethod
    async def rollback(self):
        pass

    @abc.abstractmethod
    async def close(self):
        pass

    @property
    @abc.abstractmethod
    def users(self) -> Repository[T]:
        pass


class Service:

    def __init__(self, uow: UnitOfWorkBase):
        self.uow = uow
