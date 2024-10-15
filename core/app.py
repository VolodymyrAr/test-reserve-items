# pylint: disable=unused-argument
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from core.exceptions import ObjNotFoundError, NotAllowed, ServiceError
from core.routers import api
from core.schemas import Error

app = FastAPI()
app.include_router(api, prefix="/api")


@app.exception_handler(ObjNotFoundError)
async def obj_not_found_handler(request: Request, exc: ObjNotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Error(detail=str(exc)).model_dump(),
    )


@app.exception_handler(NotAllowed)
async def not_allowed_handler(request: Request, exc: NotAllowed) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=Error(detail=str(exc)).model_dump(),
    )


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=Error(detail=str(exc)).model_dump(),
    )


@app.get("/")
async def hello():
    return {"message": "Hello World"}
