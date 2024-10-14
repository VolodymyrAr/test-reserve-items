import enum
import sqlalchemy
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db

health = APIRouter()


class Status(enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"


@health.get("/web")
async def health_check_api():
    return {"status": Status.SUCCESS.value}


@health.get("/db")
async def health_check_db(db: AsyncSession = Depends(get_db)):
    result = await db.execute(sqlalchemy.text("SELECT 1"))
    result = result.fetchall()
    if result == [(1,)]:
        return {"status": Status.SUCCESS.value}
    return {"status": Status.FAILED.value}
