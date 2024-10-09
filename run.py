import uvicorn
from fastapi import FastAPI

from core.logger import log
from core.routers import api

app = FastAPI()
app.include_router(api, prefix="/api", tags=["api"])


@app.get("/")
async def hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    log.info("Hello!")
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)  # nosec
