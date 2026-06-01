from dataclasses import dataclass
from typing import Any


@dataclass
class RunAnalysisCommand:
    user_id: str
    language: str
    code: str


@dataclass
class AnalysisView:
    analysis_id: str
    payload: dict[str, Any]
