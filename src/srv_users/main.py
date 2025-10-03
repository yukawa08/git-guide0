from features.users import health
from fastapi import FastAPI, APIRouter


def create_app() -> FastAPI:
    app = FastAPI(
        title="srv_users",
        version="0.1.0",
        docs_url="docs"
    )

    v1_router = APIRouter(prefix="/api/v1")

    v1_router.include_router(health.health_router, tags=["helth"])

    app.include_router(v1_router)

    return app