"""Entry point for the API gateway service."""

import uvicorn

from app.core.settings import settings


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.api_host, port=settings.api_port, reload=False)
