import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_db_session(db: AsyncSession):
    result = await db.execute(sqlalchemy.text("SELECT 1"))
    assert result.fetchall() == [(1,)]
