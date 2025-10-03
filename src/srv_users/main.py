from src.srv_users.features.users.api.routers.v1.health import health_router
from fastapi import FastAPI, APIRouter


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="srv_users",
        version="0.1.0",
        docs_url="/docs"
    )

    v1_router = APIRouter(prefix="/api/v1")

    v1_router.include_router(health_router, tags=["health"])

    app_.include_router(v1_router)

    return app_

app = create_app()