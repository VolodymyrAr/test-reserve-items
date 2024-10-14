import uvicorn

from core.logger import log
from core.app import app  # noqa pylint: disable=unused-import


if __name__ == "__main__":
    log.info("Hello!")
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)  # nosec
