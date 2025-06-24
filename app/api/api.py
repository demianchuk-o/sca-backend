from fastapi import APIRouter

from app.api import cat

api_router = APIRouter()
api_router.include_router(cat.router, prefix="/cats", tags=["cats"])