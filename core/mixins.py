from typing import Any

from sqlalchemy import Select


class ExecuteMixin:

    async def _execute(self, query: Select) -> Any:
        return await self.db.execute(query)

    async def _execute_one(self, query: Select) -> Any:
        resp = await self._execute(query)
        return resp.scalar_one_or_none()

    async def _execute_all(self, query: Select) -> Any:
        resp = await self._execute(query)
        return resp.scalars().all()
