import abc
from abc import ABC
from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.store.repositories import ItemRepository, CategoryRepository
from core.users.repositories import UserRepository


class UnitOfWorkBase(ABC):

    async def __aenter__(self, commit=True):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            await self.commit()
        else:
            await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        pass

    @abc.abstractmethod
    async def rollback(self):
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

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

        self._users: Optional[UserRepository] = None

        self._items: Optional[ItemRepository] = None
        self._categories: Optional[CategoryRepository] = None

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

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


async def get_uow(db: AsyncSession = Depends(get_db)) -> UnitOfWork:
    async with UnitOfWork(db) as uow:
        yield uow
