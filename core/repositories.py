from sqlalchemy.ext.asyncio import AsyncSession


class Repository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db
