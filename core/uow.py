import abc
from abc import ABC

import sqlalchemy

from .db import AsyncLocalSession


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


class UnitOfWork(UnitOfWorkBase):

    def __init__(self) -> None:
        self.db = AsyncLocalSession()

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def close(self):
        await self.db.close()

    async def health_check(self):
        result = await self.db.execute(sqlalchemy.text("SELECT 1"))
        if result.fetchall() == [(1,)]:
            return True
        return False


async def get_uow() -> UnitOfWork:
    async with UnitOfWork() as uow:
        yield uow
