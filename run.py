import uvicorn
from fastapi import FastAPI

from core.routers import health

app = FastAPI()
app.include_router(health, prefix="/api/health", tags=["health"])


@app.get("/")
async def hello():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("run:core", host="0.0.0.0", port=8000, reload=True)  # nosec
