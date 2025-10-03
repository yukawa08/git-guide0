from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["health"])

@health_router.get("/")
async def get_helth():
    return {"status": "ok"}