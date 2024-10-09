import abc
from abc import ABC
from typing import Optional

import sqlalchemy

from .db import AsyncLocalSession
from .users.repository import UserRepository


class UnitOfWorkBase(ABC):

    async def __aenter__(self):
        print(" UOW enter ")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(" UOW exit ")
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
    def users(self) -> UserRepository:
        pass


class UnitOfWork(UnitOfWorkBase):

    def __init__(self) -> None:
        self.db = AsyncLocalSession()

        self._users: Optional[UserRepository] = None

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

    @property
    def users(self) -> UserRepository:
        self._users = self._users or UserRepository(self.db)
        return self._users


async def get_uow() -> UnitOfWork:
    async with UnitOfWork() as uow:
        yield uow
