"""Application entrypoint for the FastAPI backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Configure lightweight runtime concerns during app startup."""
    configure_logging()
    yield


app = FastAPI(
    title="AI B2B Sales Knowledge Base & Lead Qualification System",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Simple health check used during the skeleton phase."""
    return {
        "status": "ok",
        "service": "ai-b2b-sales-system",
    }
