from fastapi import APIRouter

from app.api import cat, target, mission
api_router = APIRouter()
api_router.include_router(cat.router, prefix="/cats", tags=["cats"])
api_router.include_router(target.router, prefix="/targets", tags=["targets"])
api_router.include_router(mission.router, prefix="/missions", tags=["missions"])