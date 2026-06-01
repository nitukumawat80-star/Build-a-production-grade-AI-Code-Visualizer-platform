from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.analysis import AnalysisResult


class AnalysisRepository(ABC):
    @abstractmethod
    async def save(self, user_id: str, code: str, result: AnalysisResult) -> str:
        raise NotImplementedError

    @abstractmethod
    async def get(self, analysis_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_history(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        raise NotImplementedError
