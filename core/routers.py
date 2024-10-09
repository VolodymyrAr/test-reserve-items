from fastapi import APIRouter

health = APIRouter()


@health.get("/web")
async def health_check_api():
    return {"status": "ok"}


# @core.get("/health-check/db/")
# async def health_check_db(db: AsyncSession = Depends(get_session)):
#     result = await db.execute(sqlalchemy.text("SELECT 1"))
#     if result.fetchall() == [(1,)]:
#         return {"status": "ok"}
#     return {"status": "error"}
