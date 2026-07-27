from fastapi import APIRouter

from src import HealthResponse

health_router = APIRouter()


@health_router.get("/health")
async def health() -> HealthResponse:
    return HealthResponse(status="healthy")