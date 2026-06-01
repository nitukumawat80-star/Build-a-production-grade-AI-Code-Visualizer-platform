from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.services.analysis_service import AnalysisService
from app.core.config import get_settings
from app.db.session import get_db_session
from app.infrastructure.cache.redis_cache import RedisCache
from app.infrastructure.repositories.analysis_repository import PostgresAnalysisRepository
from app.schemas.analysis import AnalysisHistoryItem, AnalysisResponse, AnalysisRunRequest

router = APIRouter(prefix="/analysis", tags=["analysis"])


async def get_analysis_service(session: AsyncSession = Depends(get_db_session)) -> AnalysisService:
    settings = get_settings()
    repository = PostgresAnalysisRepository(session)
    cache = RedisCache(settings.redis_url)
    return AnalysisService(repository=repository, cache=cache)


@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(
    payload: AnalysisRunRequest,
    service: AnalysisService = Depends(get_analysis_service),
) -> dict:
    try:
        return await service.run(user_id=payload.user_id, language=payload.language, code=payload.code)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/history/{user_id}", response_model=list[AnalysisHistoryItem])
async def get_history(
    user_id: str,
    limit: int = 20,
    service: AnalysisService = Depends(get_analysis_service),
) -> list[dict]:
    return await service.get_history(user_id=user_id, limit=limit)


@router.get("/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    service: AnalysisService = Depends(get_analysis_service),
) -> dict:
    record = await service.get_by_id(analysis_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record
