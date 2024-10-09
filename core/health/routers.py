from fastapi import APIRouter, Depends

from ..uow import get_uow, UnitOfWork

health = APIRouter()


@health.get("/web")
async def health_check_api():
    return {"status": "ok"}


@health.get("/db")
async def health_check_db(uow: UnitOfWork = Depends(get_uow)):
    check_db = await uow.health_check()
    if check_db:
        return {"status": "ok"}
    return {"status": "fail"}
