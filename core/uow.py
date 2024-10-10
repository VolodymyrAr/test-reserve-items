from typing import Optional

import sqlalchemy

from core.base import UnitOfWorkBase
from core.db import AsyncLocalSession
from core.users.repositories import UserRepository


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
