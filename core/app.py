# pylint: disable=unused-argument
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from core.exceptions import ObjNotFoundError
from core.routers import api

app = FastAPI()
app.include_router(api, prefix="/api")


@app.exception_handler(ObjNotFoundError)
async def obj_not_found_handler(request: Request, exc: ObjNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": str(exc)},
    )


@app.get("/")
async def hello():
    return {"message": "Hello World"}
