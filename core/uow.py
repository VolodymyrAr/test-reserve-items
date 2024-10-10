import abc
from abc import ABC
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.db import LocalSession
from core.store.repositories import ItemRepository, CategoryRepository
from core.users.repositories import UserRepository


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
    def users(self) -> UserRepository:
        pass

    @property
    @abc.abstractmethod
    def items(self) -> ItemRepository:
        pass

    @property
    @abc.abstractmethod
    def categories(self) -> CategoryRepository:
        pass


class UnitOfWork(UnitOfWorkBase):

    def __init__(self, db: AsyncSession = None) -> None:
        self.db = db or LocalSession()

        self._users: Optional[UserRepository] = None

        self._items: Optional[ItemRepository] = None
        self._categories: Optional[CategoryRepository] = None

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def close(self):
        await self.db.close()

    @property
    def users(self) -> UserRepository:
        self._users = self._users or UserRepository(self.db)
        return self._users

    @property
    def items(self) -> ItemRepository:
        self._items = self._items or ItemRepository(self.db)
        return self._items

    @property
    def categories(self) -> CategoryRepository:
        self._categories = self._categories or CategoryRepository(self.db)
        return self._categories


async def get_uow() -> UnitOfWork:
    async with UnitOfWork() as uow:
        yield uow
