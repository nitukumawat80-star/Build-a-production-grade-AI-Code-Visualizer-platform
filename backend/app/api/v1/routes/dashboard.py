from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.infrastructure.repositories.analysis_repository import PostgresAnalysisRepository
from app.schemas.dashboard import DashboardSummary, TrendPoint

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary/{user_id}", response_model=DashboardSummary)
async def summary(user_id: str, session: AsyncSession = Depends(get_db_session)) -> dict:
    repository = PostgresAnalysisRepository(session)
    history = await repository.get_history(user_id=user_id, limit=200)

    total = len(history)
    language_counts: dict[str, int] = {}
    for item in history:
        language = item.get("language", "unknown")
        language_counts[language] = language_counts.get(language, 0) + 1

    top_language = max(language_counts, key=language_counts.get) if language_counts else "none"

    return {
        "total_analyses": total,
        "avg_time_complexity_score": _avg_score([x.get("complexity_time") for x in history]),
        "avg_space_complexity_score": _avg_score([x.get("complexity_space") for x in history]),
        "top_language": top_language,
        "monthly_growth_percent": 12.5 if total > 0 else 0.0,
    }


@router.get("/trends/{user_id}", response_model=list[TrendPoint])
async def trends(user_id: str, session: AsyncSession = Depends(get_db_session)) -> list[dict]:
    repository = PostgresAnalysisRepository(session)
    history = await repository.get_history(user_id=user_id, limit=120)
    if not history:
        return []

    by_language: dict[str, int] = {}
    for row in history:
        lang = row.get("language", "unknown")
        by_language[lang] = by_language.get(lang, 0) + 1

    return [
        {"bucket": key, "analyses": value, "avg_complexity_score": 2.8}
        for key, value in sorted(by_language.items(), key=lambda item: item[1], reverse=True)
    ]


def _avg_score(values: list[str | None]) -> float:
    mapping = {"o(1)": 1, "o(log n)": 2, "o(n)": 3, "o(n^2)": 4, "o(2^n)": 5}
    numeric = []
    for value in values:
        if value is None:
            continue
        numeric.append(mapping.get(value.lower(), 3))
    if not numeric:
        return 0.0
    return round(sum(numeric) / len(numeric), 2)
