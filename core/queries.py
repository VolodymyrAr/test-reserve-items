from sqlalchemy.ext.asyncio import AsyncSession

from core.mixins import ExecuteMixin


class Query(ExecuteMixin):

    def __init__(self, db: AsyncSession):
        self.db = db
