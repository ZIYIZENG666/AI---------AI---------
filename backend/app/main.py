"""Application entrypoint for the FastAPI backend."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from redis import Redis

from app.core.config import settings
from app.core.database import check_database_connection
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging
from app.modules.campaigns.routes import router as campaigns_router
from app.modules.company.routes import router as company_router
from app.modules.discovery.routes import router as discovery_router
from app.modules.intelligence.routes import router as intelligence_router
from app.modules.knowledge.routes import router as knowledge_router
from app.modules.products.routes import router as products_router
from app.modules.sources.routes import router as sources_router
from app.modules.tasks.routes import router as tasks_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Configure lightweight runtime concerns during app startup."""

    configure_logging()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    debug=settings.app_debug,
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(company_router, prefix="/api/v1")
app.include_router(sources_router, prefix="/api/v1")
app.include_router(knowledge_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(campaigns_router, prefix="/api/v1")
app.include_router(discovery_router, prefix="/api/v1")
app.include_router(intelligence_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    """Simple liveness check for the backend process."""

    return {
        "status": "ok",
        "service": "ai-b2b-sales-system",
    }


@app.get("/health/db", tags=["system"])
async def database_health_check():
    """Check that the configured database is reachable."""

    try:
        check_database_connection()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "database": "unavailable",
            },
        )

    return {
        "status": "ok",
        "database": "connected",
    }


@app.get("/health/redis", tags=["system"])
async def redis_health_check():
    """Check that the configured Redis endpoint responds to ping."""

    client = Redis.from_url(
        settings.redis_url,
        socket_connect_timeout=1,
        socket_timeout=1,
    )
    try:
        client.ping()
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "status": "error",
                "redis": "unavailable",
            },
        )
    finally:
        client.close()

    return {
        "status": "ok",
        "redis": "connected",
    }
