import enum
import sqlalchemy
from fastapi import APIRouter

from core.db import LocalSession

health = APIRouter()


class Status(enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"


@health.get("/web")
async def health_check_api():
    return {"status": Status.SUCCESS.value}


@health.get("/db")
async def health_check_db():
    db = LocalSession()
    result = await db.execute(sqlalchemy.text("SELECT 1"))
    result = result.fetchall()
    await db.close()
    if result == [(1,)]:
        return {"status": Status.SUCCESS.value}
    return {"status": Status.FAILED.value}
