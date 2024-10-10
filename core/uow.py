from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.base import UnitOfWorkBase
from core.db import LocalSession
from core.users.repositories import UserRepository


class UnitOfWork(UnitOfWorkBase):

    def __init__(self, db: AsyncSession = None) -> None:
        self.db = db or LocalSession()

        self._users: Optional[UserRepository] = None

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


async def get_uow() -> UnitOfWork:
    async with UnitOfWork() as uow:
        yield uow
