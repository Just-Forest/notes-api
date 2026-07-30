from fastapi import APIRouter

from src.api.endpoints import health, auth, notes

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(notes.router)
api_router.include_router(health.router)
