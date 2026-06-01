from fastapi import APIRouter

from app.api.v1.routes.analysis import router as analysis_router
from app.api.v1.routes.dashboard import router as dashboard_router
from app.api.v1.routes.exports import router as exports_router
from app.api.v1.routes.health import router as health_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(analysis_router)
api_router.include_router(dashboard_router)
api_router.include_router(exports_router)
