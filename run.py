# pylint: disable=unused-argument
import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from core.exceptions import ObjNotFoundError
from core.logger import log
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


if __name__ == "__main__":
    log.info("Hello!")
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)  # nosec
