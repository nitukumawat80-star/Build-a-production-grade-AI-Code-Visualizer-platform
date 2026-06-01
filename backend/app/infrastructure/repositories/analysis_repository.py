from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AnalysisModel
from app.domain.entities.analysis import AnalysisResult
from app.domain.interfaces.repositories import AnalysisRepository


class PostgresAnalysisRepository(AnalysisRepository):
    _memory_store: dict[str, dict[str, Any]] = {}

    def __init__(self, session: AsyncSession | None) -> None:
        self.session = session

    async def save(self, user_id: str, code: str, result: AnalysisResult) -> str:
        record_id = str(uuid.uuid4())
        payload = {
            "id": record_id,
            "user_id": user_id,
            "language": result.language,
            "source_code": code,
            "result_json": {
                "complexity": result.complexity.__dict__,
                "patterns": [p.__dict__ for p in result.patterns],
                "narration": {"en": result.narration_en, "hi": result.narration_hi},
            },
            "complexity_time": result.complexity.time,
            "complexity_space": result.complexity.space,
            "created_at": datetime.now(tz=timezone.utc).isoformat(),
        }

        self._memory_store[record_id] = payload

        if self.session is not None:
            model = AnalysisModel(
                id=uuid.UUID(record_id),
                user_id=uuid.UUID(user_id),
                language=result.language,
                source_code=code,
                result_json=payload["result_json"],
                complexity_time=result.complexity.time,
                complexity_space=result.complexity.space,
            )
            self.session.add(model)
            try:
                await self.session.commit()
            except Exception:
                try:
                    await self.session.rollback()
                except Exception:
                    pass

        return record_id

    async def get(self, analysis_id: str) -> dict[str, Any] | None:
        if analysis_id in self._memory_store:
            return self._memory_store[analysis_id]

        if self.session is None:
            return None

        stmt = select(AnalysisModel).where(AnalysisModel.id == uuid.UUID(analysis_id))
        row = (await self.session.execute(stmt)).scalar_one_or_none()
        if row is None:
            return None
        return {
            "id": str(row.id),
            "user_id": str(row.user_id),
            "language": row.language,
            "source_code": row.source_code,
            "result_json": row.result_json,
            "complexity_time": row.complexity_time,
            "complexity_space": row.complexity_space,
        }

    async def get_history(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        from_memory = [v for v in self._memory_store.values() if v["user_id"] == user_id]
        from_memory = sorted(from_memory, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

        if self.session is None:
            return from_memory

        try:
            stmt = (
                select(AnalysisModel)
                .where(AnalysisModel.user_id == uuid.UUID(user_id))
                .order_by(AnalysisModel.created_at.desc())
                .limit(limit)
            )
            rows = (await self.session.execute(stmt)).scalars().all()
            if rows:
                return [
                    {
                        "id": str(row.id),
                        "user_id": str(row.user_id),
                        "language": row.language,
                        "complexity_time": row.complexity_time,
                        "complexity_space": row.complexity_space,
                        "created_at": str(row.created_at),
                    }
                    for row in rows
                ]
        except Exception:
            return from_memory

        return from_memory
